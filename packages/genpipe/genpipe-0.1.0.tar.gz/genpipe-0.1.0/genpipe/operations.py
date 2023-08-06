from .genpipe import PipeableOperation, PipeableAggregate
from typing import TypeVar

__all__ = [
    "inc",
    "dec",
    "pow",
    "mean",
]

N = TypeVar("N", int, float)


def increment(x: N, n: N = 1) -> N:
    return x + n


inc = PipeableOperation[N, N](increment)


def decrement(x: N, n: N = 1) -> N:
    return x - n


dec = PipeableOperation[N, N](decrement)

pow = PipeableOperation[N, N](lambda x, n=2: x**n)

def mean(x: N) -> N:
    i = list(x)
    return sum(i)/len(i)
mean = PipeableAggregate[N, N](mean)
