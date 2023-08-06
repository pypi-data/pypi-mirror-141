#!/usr/bin/env python

import typing as t
from abc import ABC, abstractmethod

from orbiteer.optimizers import AbstractOptimizer

IT = t.TypeVar("IT")  # InputType - the type used to talk about the input values themselves


class AbstractInputGenerator(t.Generic[IT], ABC):
    """
    An input generator generates input for the operation. Implementations should have some way of configuring source
    data. When the optimizer computes the next interval size, the input generator should use that to compute the next
    actual inputs.
    """

    def __init__(self, optimizer: AbstractOptimizer, *args: t.Any, **kwargs: t.Any) -> None:
        self.optimizer = optimizer

    def compute_next_input(self, last_measurement: t.Optional[float]) -> t.Iterable[str]:
        if not self.is_done:
            next_interval = self.optimizer.compute_next(last_measurement)
            return self._coerce_input(self._compute_next_input(next_interval))
        else:
            raise StopIteration

    @property
    def is_done(self) -> bool:
        """
        Whether or not there are more things to iterate over. Once false, should never become true again.
        """
        return self._is_done()

    def _coerce_input(self, next_input: t.Iterable[IT]) -> t.Iterable[str]:
        """
        Converts the next input(s) into strings
        """
        return [str(i) for i in next_input]

    @abstractmethod
    def _compute_next_input(self, next_interval: float) -> t.Iterable[IT]:
        """
        Computes the next parameters to feed to the command for the next run
        """

    @abstractmethod
    def _is_done(self) -> bool:
        """
        Tells whether or not we are done
        """
