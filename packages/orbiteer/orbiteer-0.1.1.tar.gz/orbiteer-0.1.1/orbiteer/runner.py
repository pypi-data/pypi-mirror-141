#!/usr/bin/env python

import typing as t

import orbiteer.inputgenerators as inputgenerators
import orbiteer.targets as targets

RT = t.TypeVar("RT")


class OrbiteerRunner:
    def __init__(
        self,
        inputgenerator: inputgenerators.AbstractInputGenerator[RT],
        target: targets.AbstractTarget,
    ) -> None:
        self.inputgenerator = inputgenerator
        self.target = target

    def run(self) -> None:
        first_range = self.inputgenerator.compute_next_input(None)
        next_range = first_range

        while not self.inputgenerator.is_done:
            measurement = self.target.run(next_range)
            next_range = self.inputgenerator.compute_next_input(measurement)
