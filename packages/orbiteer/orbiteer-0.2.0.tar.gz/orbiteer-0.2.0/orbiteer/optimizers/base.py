#!/usr/bin/env python

import typing as t
from abc import ABC, abstractmethod

from typing_extensions import Literal


class AbstractOptimizer(ABC):
    """
    An Optimizer is responsible for calculating the next interval for each operation
    """

    def __init__(
        self,
        goal: float,
        first_value: float,
        max_value: t.Optional[float] = None,
        min_value: t.Optional[float] = None,
        round_places: t.Union[int, Literal[False]] = 0,
    ) -> None:
        self.goal = goal
        self.max_value = max_value
        self.min_value = min_value
        self.outputs = [first_value]
        self.round_places = round_places

    def compute_next(self, measurement: t.Optional[float]) -> float:
        if measurement is None:
            return self.outputs[0]

        next_value = self._compute_next(measurement)
        next_value = self._limit_value(next_value)
        next_value = self._round_value(next_value)
        self.outputs.append(next_value)

        return next_value

    @abstractmethod
    def _compute_next(self, measurement: float) -> float:
        """
        Computes the next raw size of the input generator, without limits
        """

    def _limit_value(self, next_value: float) -> float:
        if self.max_value is not None:
            next_value = min(self.max_value, next_value)
        if self.min_value is not None:
            next_value = max(self.min_value, next_value)
        return next_value

    def _round_value(self, next_value: float) -> float:
        # In this case, round_places can only be an int or literally "false", so, checking for truthiness is not
        # correct.
        return round(next_value, self.round_places) if self.round_places is not False else next_value
