from typing import (
    Protocol,
    Generator,
    Iterable,
    Optional,
    TypeVar,
    Union,
    runtime_checkable,
)

# T is the input type to a `Pipeable`
T = TypeVar("T")
# V is the output tipe to a `Pipeable`
V = TypeVar("V")


@runtime_checkable
class Pipeable(Protocol[T, V]):
    def execute(self) -> Union[Generator[V, None, None], V]:
        ...

    def copy(self, stream: Optional[Iterable[T]]) -> "Pipeable[T, V]":
        ...

    def __or__(self, right: "Pipeable[T, V]") -> "Pipeable[T, V]":
        ...

    def __ror__(self, left: Iterable[V]) -> "Pipeable[T, V]":
        ...
