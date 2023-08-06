#!/usr/bin/env python

import typing as t
from abc import ABC
from datetime import datetime, timedelta

from typing_extensions import Final, Protocol

from .base import AbstractInputGenerator

T = t.TypeVar("T")


class SelfComparable(Protocol):
    def __ge__(self: T, other: T) -> bool:
        ...

    def __eq__(self: T, other: t.Any) -> bool:
        ...

    def __lt__(self: T, other: T) -> bool:
        ...


ART = t.TypeVar("ART", bound=SelfComparable)


class AbstractRangeGenerator(AbstractInputGenerator[ART], ABC):
    def __init__(self, *args: t.Any, left: ART, right: ART, **kwargs: t.Any) -> None:
        # default is new to old == left -> right
        self.reverse_order = kwargs.pop("reverse_order", False)
        self.left = left
        self.right = right

        if not self.reverse_order:
            self.end = self.right
            self.right = self.left
        else:
            self.end = self.left
            self.left = self.right

        super().__init__(*args, **kwargs)

    def _is_done(self) -> bool:
        if not self.reverse_order:
            return self.left >= self.end
        else:
            return self.right <= self.end


class NumbericalRangeType(Protocol):
    """
    Protocol to define needs of interaction between T and float
     w"""

    def __add__(self: T, other: float) -> T:
        ...

    def __sub__(self: T, other: float) -> T:
        ...

    def __ge__(self: T, other: t.Any) -> bool:
        ...

    def __eq__(self: T, other: t.Any) -> bool:
        ...

    def __lt__(self: T, other: t.Any) -> bool:
        ...


RT = t.TypeVar("RT", bound=NumbericalRangeType)


class NumericalRangeGenerator(AbstractRangeGenerator[RT]):
    def _compute_next_input(self, next_interval: float) -> t.Tuple[RT, RT]:
        if not self.reverse_order:
            self.left = self.right
            self.right = min(self.left + next_interval, self.end)
        else:
            self.right = self.left
            self.left = max(self.right - next_interval, self.end)

        return self.left, self.right


class DatetimeRangeGenerator(AbstractRangeGenerator[datetime]):
    MAGIC_USE_ISOFORMAT: Final = "MAGIC_USE_ISOFORMAT"

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.datetime_format = kwargs.pop("format", self.MAGIC_USE_ISOFORMAT)

        super().__init__(*args, **kwargs)

    def _compute_next_input(self, next_interval: float) -> t.Tuple[datetime, datetime]:
        converted_interval = timedelta(seconds=next_interval)

        if not self.reverse_order:
            self.left = self.right
            self.right = min(self.left + converted_interval, self.end)
        else:
            self.right = self.left
            self.left = max(self.right - converted_interval, self.end)

        return self.left, self.right

    def _convert_datetime_to_str(self, dt: datetime) -> str:
        if self.datetime_format is self.MAGIC_USE_ISOFORMAT:
            return dt.isoformat()
        else:
            return dt.strftime(self.datetime_format)

    def _coerce_input(self, next_input: t.Iterable[datetime]) -> t.List[str]:
        """
        Converts datetimes to pretty strings

        TODO make this more configurable
        """
        return [self._convert_datetime_to_str(i) for i in next_input]
