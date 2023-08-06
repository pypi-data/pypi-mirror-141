from typing import (
    Callable,
    Generic,
    Generator,
    Iterable,
    Optional,
    TypeVar,
    Any,
)
from collections.abc import Iterable as TIterable
from .protocol import Pipeable, T, V


class PipeableOperation(Pipeable[T, V]):
    """PipeableOperation implements `map + filter` via the | operator.

    :param operation: A Callable that will be called for every record in the input
        stream.
    :param *args: Optional arbitrary positional args to be passed to operation. Note,
        the first arg to ``operation`` will _always_ be a value from the input stream.
        Thesse values will apply to every usage of a given instance of
        ``PipeableOperation``. If you wish to have parameters that only apply to a given
        *operation* on a datastream, use the `ds | op(myarg)` syntax instead, as it will
        prevent unwanted arguments from being passed in.
    :param stream: (Optional) an iterable source of data. All values that would be
        returned by next(stream) get passed as the first argument to ``operation``. It
        normally shouldn't be necessary to set this here, as when using the `iterable |
        PipeableOperation` syntax, the stream is source from the output of the value to
        the left of the `|`, including any previous transformations in the pipe chain.
    :param **kwargs: (Optional) arbitrary kwargs get passed to ``operation`` upon
        execution.If you wish to have parameters that only apply to a given *operation*
        on a datastream, use the `ds | op(myarg=value)` syntax instead, as it will
        prevent unwanted arguments from being passed in.
    """

    def __init__(
        self,
        operation: Callable[..., V],
        *args,
        stream: Optional[Iterable[V]] = None,
        **kwargs,
    ):
        self.operation = operation
        self.args: tuple = args
        self.kwargs: dict = kwargs
        self.stream = stream

    def execute(self) -> Generator[V, None, None]:
        if self.stream is None:
            raise ValueError("Attempting to execute on an empty stream")
        for d in self.stream:
            if not self.args and not self.kwargs:
                yield self.operation(d)
            elif self.args and not self.kwargs:
                yield self.operation(d, *self.args)
            elif not self.args and self.kwargs:
                yield self.operation(d, **self.kwargs)
            else:
                yield self.operation(d, *self.args, **self.kwargs)

    def copy(
        self, stream: Optional[Iterable[V]]
    ) -> "PipeableOperation[T, V]":
        """copy returns a new instance of a ``PipeableOperation`` with the same
        operation, args, kwargs, and optionally a new stream."""
        return self.__class__(self.operation, *self.args, stream=stream, **self.kwargs)

    def __call__(self, *args, **kwargs) -> "PipeableOperation[T, V]":
        return self.__class__(self.operation, *args, stream=self.stream, **kwargs)

    def __or__(self, right: "Pipeable[T, V]") -> "Pipeable[T, V]":
        if not isinstance(right, Pipeable):
            return NotImplemented
        n = right.copy(self.execute())
        return n

    def __ror__(self, left: Iterable[V]) -> "Pipeable[T, V]":
        if not isinstance(left, TIterable):
            return NotImplemented
        return self.copy(left)


class PipeableAggregate(Pipeable[T, V]):
    def __init__(
        self,
        operation: Callable[..., V],  # ... is Iterable[T]
        *args,
        stream: Optional[Iterable[T]] = None,
        **kwargs,
    ):
        self.operation = operation
        self.args: tuple = args
        self.kwargs: dict = kwargs
        self.stream = stream

    def execute(self) -> V:
        if self.stream is None:
            raise ValueError("Attempting to execute on an empty stream")
        if not self.args and not self.kwargs:
            return self.operation(self.stream)
        elif self.args and not self.kwargs:
            return self.operation(self.stream, *self.args)
        elif not self.args and self.kwargs:
            return self.operation(self.stream, **self.kwargs)
        else:
            return self.operation(self.stream, *self.args, **self.kwargs)

    def copy(
        self, stream: Optional[Iterable[T]]
    ) -> "Pipeable[T, V]":
        """copy returns a new instance of a ``PipeableOperation`` with the same
        operation, args, kwargs, and optionally a new stream."""
        return self.__class__(self.operation, *self.args, stream=stream, **self.kwargs)

    def __call__(self, *args, **kwargs) -> "Pipeable[T, V]":
        return self.__class__(self.operation, *args, stream=self.stream, **kwargs)

    def __ror__(self, left: Iterable[V]) -> "Pipeable[T, V]":
        if not isinstance(left, TIterable):
            return NotImplemented
        return self.copy(left)
