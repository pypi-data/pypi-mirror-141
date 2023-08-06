#!/usr/bin/env python

import typing as t

from .base import AbstractOptimizer


class RatioOptimizer(AbstractOptimizer):
    """
    The Ratio optimizer simply takes the last measurement and the goal measurement, and uses the ratio found to modify
    the last interval computed.

    Optionally, a damper can be used to limit the magnitude of effect.
    """

    def __init__(
        self,
        *args: t.Any,
        damper: float = 1.0,  # Should be less than 1.0 to have damping effect
        **kwargs: t.Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.damper = damper

    def _compute_next(self, measurement: float) -> float:
        """
        Computes the direct ratio of where we are compared to where we want to be and uses it as a multiplier.

        If the measurement is exactly zero, the last value will be returned again.
        """
        last_output = self.outputs[-1]

        if measurement == 0.0:
            return last_output

        direct_ratio = self.goal / measurement

        # This damps and equalizes the ratio as required
        # Being damped by .X means that the change is only X% as strong. A damper of 0.5 would mean a 50% as strong mult
        multiplier = 1 + (direct_ratio - 1) * self.damper

        return last_output * multiplier
