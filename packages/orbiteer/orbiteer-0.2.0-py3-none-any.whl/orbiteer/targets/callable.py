#!/usr/bin/env python

import typing as t

from .base import AbstractTarget, TargetMeasurementStrategy


class CallableTarget(AbstractTarget):
    def __init__(
        self,
        *args: t.Any,
        to_call: t.Optional[t.Callable[..., t.Optional[float]]] = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        if to_call is None:
            raise ValueError("to_call must be present")

        self.to_call = to_call

    def _run_target(self, inputs: t.Iterable[str]) -> t.Optional[float]:
        output = self.to_call(*inputs)

        # No need to try (and potentially fail) a float conversion if we aren't using that value
        if self.measurement_strategy == TargetMeasurementStrategy.OUTPUT:
            return float(output) if output is not None else output
        else:
            return None
