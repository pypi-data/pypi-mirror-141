#!/usr/bin/env python

import enum
from abc import ABC, abstractmethod


class TargetMeasurementStrategy(enum.Enum):
    DURATION = "Command Duration"
    STDOUT = "Command stdout"


class Options(ABC):
    @abstractmethod
    @property
    def target_measurement_strategy(self) -> TargetMeasurementStrategy:
        """
        Which measurement strategy are we using to optimize on?
        """
