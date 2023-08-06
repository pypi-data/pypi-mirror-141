from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Generator, List


class EventNotification:
    """
    EventNotification implements basic [Event-driven messaging](https://en.wikipedia.org/wiki/Event-driven_messaging).

    >>> meeting = EventNotification()
    >>> attendees = []
    >>> meeting += lambda: attendees.append("Alice")
    >>> meeting += lambda: attendees.append("Bob")
    >>> meeting()
    >>> attendees
    ['Alice', 'Bob']
    """

    __slots__ = ("listeners",)

    @staticmethod
    def notify(listener: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        listener(*args, **kwargs)

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._init_listeners()

    def _init_listeners(self) -> None:
        self.listeners: List[Callable[..., Any]] = list()

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        for listener in self.listeners:
            self.notify(listener, *args, **kwargs)

    def __add__(self, other: Callable[..., Any]) -> EventNotification:
        return self.register(other)

    def __iadd__(self, other: Callable[..., Any]) -> EventNotification:
        return self.__add__(other)

    def __sub__(self, other: Callable[..., Any]) -> EventNotification:
        return self.unregister(other)

    def __isub__(self, other: Callable[..., Any]) -> EventNotification:
        return self.__sub__(other)

    def register(self, _callable: Callable[..., Any]) -> EventNotification:
        """
        Register an event listener.

        This event listener will be called after all other registered event listeners (if any).
        """
        self.listeners.append(_callable)
        return self

    def unregister(self, _callable: Callable[..., Any]) -> EventNotification:
        """
        Unregister an event listener.
        """
        self.listeners.remove(_callable)
        return self

    @contextmanager
    def registering(
        self, _callable: Callable[..., Any]
    ) -> Generator[EventNotification, None, None]:
        """
        Create a context manager that registers the event listener at entering and unregisters at exiting.
        Register an event listener
        """
        try:
            self.register(_callable)
            yield self
        finally:
            self.unregister(_callable)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
