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
        next_parameters = self.inputgenerator.compute_next_input(None)

        while not self.inputgenerator.is_done:
            measurement = self.target.run(next_parameters)
            next_parameters = self.inputgenerator.compute_next_input(measurement)
