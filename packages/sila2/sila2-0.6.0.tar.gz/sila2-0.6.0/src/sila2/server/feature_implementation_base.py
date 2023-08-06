from __future__ import annotations

import time
from threading import Event
from typing import TYPE_CHECKING, Any, Callable, List

if TYPE_CHECKING:
    from sila2.server import SilaServer


_STOP_THREAD_CHECK_PERIOD: float = 0.1


class FeatureImplementationBase:
    __stop_event: Event
    __is_running: bool
    __started: bool
    __periodic_funcs: List[Callable[[], None]]
    parent_server: SilaServer

    def __init__(self, parent_server: SilaServer):
        self.parent_server = parent_server
        self.__stop_event = Event()
        self.__started = False
        self.__is_running = False
        self.__periodic_funcs = []

    @property
    def is_running(self) -> bool:
        return self.__is_running

    def start(self) -> None:
        """
        This method is called by the SiLA server when it starts serving this feature implementation
        (can only be called once)
        """
        if self.__started:
            raise RuntimeError("Cannot start feature implementation twice")
        self.__is_running = True
        self.__started = True

        for func in self.__periodic_funcs:
            self.parent_server.child_task_executor.submit(func)

    def stop(self) -> None:
        """This method is called by the SiLA server when it starts serving this feature implementation"""
        self.__stop_event.set()
        self.__is_running = False

    def run_periodically(self, func: Callable[[], Any], delay_seconds: float = _STOP_THREAD_CHECK_PERIOD) -> None:
        """Register a function to be called periodically while the SiLA server is running"""
        if delay_seconds <= _STOP_THREAD_CHECK_PERIOD:

            def looped_func():
                while not self.__stop_event.is_set():
                    func()
                    time.sleep(delay_seconds)

        else:

            def looped_func():
                nonlocal delay_seconds
                n_checks_per_loop = int(delay_seconds / _STOP_THREAD_CHECK_PERIOD)
                delay_seconds /= n_checks_per_loop

                must_stop: bool = False

                while not must_stop:
                    func()
                    for _ in range(n_checks_per_loop):
                        if self.__stop_event.is_set():
                            must_stop = True
                            break
                        time.sleep(delay_seconds)

        self.__periodic_funcs.append(looped_func)

        if self.is_running:
            self.parent_server.child_task_executor.submit(looped_func)
