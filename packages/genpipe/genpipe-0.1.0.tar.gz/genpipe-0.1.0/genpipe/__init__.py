__version__ = "0.1.0"

from .genpipe import PipeableOperation, PipeableAggregate
from .operations import inc, dec, pow, mean

__all__ = [
    "PipeableOperation",
    "inc",
    "dec",
    "pow",
    "mean",
]
