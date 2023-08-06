import asyncio
import atexit
import concurrent.futures
import functools
import inspect
import queue
import threading
import time
import warnings

from .contextlib import AsyncGeneratorContextManager
from .exceptions import UserCodeException, unwrap_coro_exception, wrap_coro_exception
from .interface import Interface

_BUILTIN_ASYNC_METHODS = {
    "__aiter__": "__iter__",
    "__aenter__": "__enter__",
    "__aexit__": "__exit__",
}

_WRAPPED_ATTR = "_SYNCHRONICITY_HAS_WRAPPED_THIS_ALREADY"
_RETURN_FUTURE_KWARG = "_future"


class Synchronizer:
    """Helps you offer a blocking (synchronous) interface to asynchronous code."""

    def __init__(
        self,
        multiwrap_warning=False,
        async_leakage_warning=True,
    ):
        self._multiwrap_warning = multiwrap_warning
        self._async_leakage_warning = async_leakage_warning
        self._loop = None
        self._thread = None
        atexit.register(self._close_loop)

    def __getstate__(self):
        return {
            "_multiwrap_warning": self._multiwrap_warning,
            "_async_leakage_warning": self._async_leakage_warning,
        }

    def __setstate__(self, d):
        self._multiwrap_warning = d["_multiwrap_warning"]
        self._async_leakage_warning = d["_async_leakage_warning"]

    def _start_loop(self, loop):
        if self._loop and self._loop.is_running():
            raise Exception("Synchronicity loop already running.")

        is_ready = threading.Event()

        def run_forever():
            self._loop = loop
            is_ready.set()
            self._loop.run_forever()

        self._thread = threading.Thread(target=lambda: run_forever(), daemon=True)
        self._thread.start()  # TODO: we should join the thread at some point
        is_ready.wait()  # TODO: this might block for a very short time
        return self._loop

    def _close_loop(self):
        if self._loop is not None and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
            while self._loop.is_running():
                time.sleep(0.01)
            self._loop.close()
        if self._thread is not None:
            self._thread.join()

    def _get_loop(self):
        if self._loop is not None:
            return self._loop
        return self._start_loop(asyncio.new_event_loop())

    def _get_running_loop(self):
        if hasattr(asyncio, "get_running_loop"):
            try:
                return asyncio.get_running_loop()
            except RuntimeError:
                return
        else:
            # Python 3.6 compatibility
            return asyncio._get_running_loop()

    def _get_runtime_interface(self, interface):
        """Returns one out of Interface.ASYNC or Interface.BLOCKING"""
        if interface == Interface.AUTODETECT:
            return Interface.ASYNC if self._get_running_loop() else Interface.BLOCKING
        else:
            assert interface in (Interface.ASYNC, Interface.BLOCKING)
            return interface

    def _wrap_check_async_leakage(self, coro):
        """Check if a coroutine returns another coroutine (or an async generator) and warn.

        The reason this is important to catch is that otherwise even synchronized code might end up
        "leaking" async code into the caller.
        """
        if not self._async_leakage_warning:
            return coro

        async def coro_wrapped():
            value = await coro
            # TODO: we should include the name of the original function here
            if inspect.iscoroutine(value):
                warnings.warn(
                    f"Potential async leakage: coroutine returned a coroutine {value}."
                )
            elif inspect.isasyncgen(value):
                warnings.warn(
                    f"Potential async leakage: Coroutine returned an async generator {value}."
                )
            return value

        return coro_wrapped()

    def _run_function_sync(self, coro):
        coro = wrap_coro_exception(coro)
        coro = self._wrap_check_async_leakage(coro)
        loop = self._get_loop()
        fut = asyncio.run_coroutine_threadsafe(coro, loop)
        return fut.result()

    def _run_function_sync_future(self, coro):
        coro = wrap_coro_exception(coro)
        coro = self._wrap_check_async_leakage(coro)
        loop = self._get_loop()
        coro = unwrap_coro_exception(coro)  # A bit of a special case
        return asyncio.run_coroutine_threadsafe(coro, loop)

    async def _run_function_async(self, coro):
        coro = wrap_coro_exception(coro)
        coro = self._wrap_check_async_leakage(coro)
        current_loop = self._get_running_loop()
        loop = self._get_loop()
        if loop == current_loop:
            return await coro

        c_fut = asyncio.run_coroutine_threadsafe(coro, loop)
        a_fut = asyncio.wrap_future(c_fut)
        return await a_fut

    def _run_generator_sync(self, gen):
        value, is_exc = None, False
        while True:
            try:
                if is_exc:
                    value = self._run_function_sync(gen.athrow(value))
                else:
                    value = self._run_function_sync(gen.asend(value))
            except UserCodeException as uc_exc:
                raise uc_exc.exc from None
            except StopAsyncIteration:
                break
            try:
                value = yield value
                is_exc = False
            except BaseException as exc:
                value = exc
                is_exc = True

    async def _run_generator_async(self, gen, unwrap_user_excs=True):
        value, is_exc = None, False
        while True:
            try:
                if is_exc:
                    value = await self._run_function_async(gen.athrow(value))
                else:
                    value = await self._run_function_async(gen.asend(value))
            except UserCodeException as uc_exc:
                if unwrap_user_excs:
                    raise uc_exc.exc from None
                else:
                    # This is needed since contextlib uses this function as a helper
                    raise uc_exc
            except StopAsyncIteration:
                break
            try:
                value = yield value
                is_exc = False
            except BaseException as exc:
                value = exc
                is_exc = True

    def _wrap_callable(self, f, interface, allow_futures=True):
        if hasattr(f, _WRAPPED_ATTR):
            if self._multiwrap_warning:
                warnings.warn(
                    f"Function {f} is already wrapped, but getting wrapped again"
                )
            return f

        @functools.wraps(f)
        def f_wrapped(*args, **kwargs):
            return_future = kwargs.pop(_RETURN_FUTURE_KWARG, False)
            res = f(*args, **kwargs)
            is_coroutine = inspect.iscoroutine(res)
            is_asyncgen = inspect.isasyncgen(res)
            runtime_interface = self._get_runtime_interface(interface)

            if return_future:
                if not allow_futures:
                    raise Exception("Can not return future for this function")
                elif is_coroutine:
                    return self._run_function_sync_future(res)
                elif is_asyncgen:
                    raise Exception("Can not return futures for generators")
                else:
                    return res
            elif is_coroutine:
                # The run_function_* may throw UserCodeExceptions that
                # need to be unwrapped here at the entrypoint
                if runtime_interface == Interface.ASYNC:
                    if self._get_running_loop() == self._get_loop():
                        # See #27. This is a bit of a hack needed to "shortcut" the exception
                        # handling if we're within the same loop - there's no need to wrap and
                        # unwrap the exception and it just adds unnecessary traceback spam.
                        return res
                    coro = self._run_function_async(res)
                    coro = unwrap_coro_exception(coro)
                    return coro
                elif runtime_interface == Interface.BLOCKING:
                    try:
                        return self._run_function_sync(res)
                    except UserCodeException as uc_exc:
                        raise uc_exc.exc from None
            elif is_asyncgen:
                # Note that the _run_generator_* functions handle their own
                # unwrapping of exceptions (this happens during yielding)
                if runtime_interface == Interface.ASYNC:
                    return self._run_generator_async(res)
                elif runtime_interface == Interface.BLOCKING:
                    return self._run_generator_sync(res)
            else:
                return res

        setattr(f_wrapped, _WRAPPED_ATTR, True)
        return f_wrapped

    def create_class(self, cls_metaclass, cls_name, cls_bases, cls_dict, interface=Interface.AUTODETECT):
        new_dict = {}
        for k, v in cls_dict.items():
            if k in _BUILTIN_ASYNC_METHODS:
                k_sync = _BUILTIN_ASYNC_METHODS[k]
                new_dict[k] = v
                new_dict[k_sync] = self._wrap_callable(
                    v, interface, allow_futures=False
                )
            elif callable(v):
                new_dict[k] = self._wrap_callable(v, interface)
            elif isinstance(v, staticmethod):
                # TODO(erikbern): this feels pretty hacky
                new_dict[k] = staticmethod(self._wrap_callable(v.__func__, interface))
            elif isinstance(v, classmethod):
                # TODO(erikbern): this feels pretty hacky
                new_dict[k] = classmethod(self._wrap_callable(v.__func__, interface))
            else:
                new_dict[k] = v
        return type.__new__(cls_metaclass, cls_name, cls_bases, new_dict)

    def _wrap_class(self, cls, interface):
        cls_metaclass = type
        cls_name = cls.__name__
        cls_bases = (cls,)
        cls_dict = cls.__dict__
        return self.create_class(
            cls_metaclass, cls_name, cls_bases, cls_dict, interface
        )

    def _wrap(self, object, interface):
        if inspect.isclass(object):
            return self._wrap_class(object, interface)
        elif callable(object):
            return self._wrap_callable(object, interface)
        else:
            raise Exception("Argument %s is not a class or a callable" % object)

    def wrap_async(self, object):
        return self._wrap(object, Interface.ASYNC)

    def wrap_blocking(self, object):
        return self._wrap(object, Interface.BLOCKING)

    def wrap_autodetect(self, object):
        # TODO(erikbern): deprecate?
        return self._wrap(object, Interface.AUTODETECT)

    def __call__(self, object):
        return self.wrap_autodetect(object)

    def asynccontextmanager(self, func, interface=Interface.AUTODETECT):
        # TODO(erikbern): enforce defining the interface type

        @functools.wraps(func)
        def helper(*args, **kwargs):
            return AsyncGeneratorContextManager(self, interface, func, args, kwargs)

        return helper
