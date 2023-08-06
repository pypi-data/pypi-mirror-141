#!/usr/bin/env python

import enum
import time
import typing as t
from abc import ABC, abstractmethod

from typing_extensions import Protocol


class Stringable(Protocol):
    def __str__(self) -> str:
        ...


class TargetMeasurementStrategy(enum.Enum):
    DURATION = "duration"
    OUTPUT = "output"


class AbstractTarget(ABC):
    """
    Targets are anything that do something with a set of inputs.
    """

    def __init__(self, measurement_strategy: TargetMeasurementStrategy = TargetMeasurementStrategy.DURATION) -> None:
        self.measurement_strategy = measurement_strategy

    @property
    def measurement_strategy(self) -> TargetMeasurementStrategy:
        return self._measurement_strategy

    @measurement_strategy.setter
    def measurement_strategy(self, new_value: TargetMeasurementStrategy) -> None:
        self._measurement_strategy = new_value

    @abstractmethod
    def _run_target(self, inputs: t.Iterable[str]) -> t.Optional[float]:
        """
        Runs the target and returns its output. Should be internally idempotent, meaning that internal state changes
        should be idempotent, but it is understood that not all possible actions are idempotent.

        Should return a measurement generated from the target directly.
        """

    def run(self, inputs: t.Iterable[Stringable]) -> float:
        """
        Runs the target and returns the measurement found.
        """
        time_before_run = time.time()
        output = self._run_target([str(i) for i in inputs])
        duration = time.time() - time_before_run

        if self.measurement_strategy == TargetMeasurementStrategy.DURATION:
            return duration
        elif self.measurement_strategy == TargetMeasurementStrategy.OUTPUT:
            if output is not None:
                return output
            else:
                return 0
        else:
            raise RuntimeError("Invalid measurement strategy")
