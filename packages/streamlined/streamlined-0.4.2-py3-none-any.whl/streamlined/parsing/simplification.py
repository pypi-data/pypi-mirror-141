from functools import partial
from typing import Any, List, Tuple

from ..common import Predicate, Transform


class Simplification:
    """
    Reduce multiple config formats to more standard formats.

    Simplification
    ------

    The most important attribute for Simplification is `simplifications`.
    This should be a list holding tuples of predicate and transform
    functions. Predicate decides whether current value need to be
    simplified and transform decides how to simplify current value.

    In order to fully simplify a value, more general (primitive)
    simplifications should precede those apply specifically.
    """

    __slots__ = ("simplifications",)

    def __init__(self) -> None:
        self._init_simplifications()
        super().__init__()

    @classmethod
    def aggregate(cls, simplifications: List[Tuple[Predicate, Transform]]) -> Transform:
        """
        Create a Transform function from a list of simplifications.

        This Transform function will be the application of these
        simplifications.
        """
        return partial(cls.simplify_with, simplifications)

    @classmethod
    def simplify_with(cls, simplifications: List[Tuple[Predicate, Transform]], value: Any) -> Any:
        """
        Using a list of simplifications to simplify a value.
        """
        simplified_value = value

        for predicate, transform in simplifications:
            if predicate(simplified_value):
                simplified_value = transform(simplified_value)

        return simplified_value

    def _init_simplifications(self) -> None:
        self.simplifications: List[Tuple[Predicate, Transform]] = []

    def simplify(self, value: Any) -> Any:
        """
        Simplify a value with registered simplifications.
        """
        return self.simplify_with(self.simplifications, value)
