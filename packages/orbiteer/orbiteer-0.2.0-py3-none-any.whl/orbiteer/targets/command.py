#!/usr/bin/env python

import subprocess
import typing as t

from .base import AbstractTarget, TargetMeasurementStrategy


class CommandTarget(AbstractTarget):
    def __init__(
        self,
        *args: t.Any,
        command_line: t.Optional[t.List[str]] = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        if command_line is None:
            raise ValueError("command_line must be present")

        self.command_line = command_line

    def _run_target(self, inputs: t.Iterable[str]) -> t.Optional[float]:
        # Its a waste to capture output if we're not using it for measurements
        capture_output = self.measurement_strategy == TargetMeasurementStrategy.OUTPUT
        stdout = subprocess.run(
            [*self.command_line, *inputs],  # Given command plus the range parameters appended
            capture_output=capture_output,
            check=True,  # Raises an error if the command fails
            text=True,  # If we have stdout, forces it into str form
        ).stdout

        # stdout _can_ be None, despite current mypy restrictions
        # https://github.com/python/typeshed/blob/bc19a28c0dd4876788bd9a5a0deedc20211cd9af/stdlib/subprocess.pyi#L43
        # TODO return based on capture_output instead - we want errors if none and should not be
        if stdout is not None:
            return float(stdout)
        else:
            return None  # type: ignore
