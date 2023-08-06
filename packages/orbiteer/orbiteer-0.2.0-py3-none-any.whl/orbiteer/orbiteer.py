#!/usr/bin/env python

import typing as t

import orbiteer.inputgenerators as inputgenerators
import orbiteer.optimizers as optimizers
import orbiteer.runner as runner
import orbiteer.targets as targets


class Orbiteer:
    input_generator_name_map = {
        "range": inputgenerators.NumericalRangeGenerator,
        "datetime_range": inputgenerators.DatetimeRangeGenerator,
    }

    target_name_map = {
        "command": targets.CommandTarget,
        "callable": targets.CallableTarget,
    }

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.target = self.make_target(**self._filter_kwargs("target", **kwargs))
        self.optimizer = self.make_optimizer(**self._filter_kwargs("optimizer", **kwargs))
        self.inputgenerator = self.make_inputgenerator(
            optimizer=self.optimizer, **self._filter_kwargs("inputgenerator", **kwargs)
        )

        self.runner = runner.OrbiteerRunner(self.inputgenerator, self.target)

    def run(self) -> None:
        self.runner.run()

    def make_target(self, **kwargs: t.Any) -> targets.AbstractTarget:
        target_type = self._pop_required_kwarg_or_raise("type", kwargs, "command")

        name = target_type.lower()
        if name in self.target_name_map:
            target_class = self.target_name_map[name]
        else:
            raise RuntimeError(f"Invalid target_type: {type}")

        try:
            return target_class(**kwargs)
        except TypeError as e:
            raise RuntimeError("Failed to create Target class") from e

    def make_optimizer(self, **kwargs: t.Any) -> optimizers.AbstractOptimizer:
        optimizer_type = self._pop_required_kwarg_or_raise("type", kwargs, "ratio")

        if optimizer_type.lower() == "ratio":
            optimizer_class = optimizers.RatioOptimizer
        else:
            raise RuntimeError(f"Invalid optimizer_type: {type}")

        try:
            return optimizer_class(**kwargs)
        except TypeError as e:
            raise RuntimeError("Failed to create Optimizer class") from e

    def make_inputgenerator(self, **kwargs: t.Any) -> inputgenerators.AbstractInputGenerator[t.Any]:
        inputgenerator_type = self._pop_required_kwarg_or_raise("type", kwargs)

        name = inputgenerator_type.lower()
        if name in self.input_generator_name_map:
            inputgenerator_class = self.input_generator_name_map[name]
        else:
            raise RuntimeError(f"Invalid inputgenerator_type: {type}")

        try:
            return inputgenerator_class(**kwargs)
        except TypeError as e:
            raise RuntimeError("Failed to create InputGenerator class") from e

    def _filter_kwargs(self, prefix: str, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        # When python3.8 support is dropped, can use str.removeprefix(). Until then, this slices the prefix and trailing
        # underscore from the kwarg key
        key_offset = len(prefix) + 1
        return {key[key_offset:]: value for key, value in kwargs.items() if key.startswith(prefix)}

    def _pop_required_kwarg_or_raise(self, key: str, kwargs: t.Dict[str, t.Any], default: t.Any = None) -> t.Any:
        value = kwargs.pop(key, default)
        if value is None:
            raise RuntimeError(f"Missing required argument: {key}")

        return value
