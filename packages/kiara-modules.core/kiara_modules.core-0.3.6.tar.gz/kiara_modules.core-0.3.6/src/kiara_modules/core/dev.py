# -*- coding: utf-8 -*-

"""Modules that are useful for kiara as well as pipeline-development, as well as testing."""

import time
import typing

from kiara import KiaraModule
from kiara.data import ValueSet
from kiara.data.values import ValueSchema
from kiara.module_config import ModuleTypeConfigSchema
from pydantic import Field


class DummyProcessingModuleConfig(ModuleTypeConfigSchema):
    """Configuration for the 'dummy' processing module."""

    documentation: typing.Optional[str] = None

    input_schema: typing.Dict[str, typing.Dict] = Field(
        description="The input schema for this module."
    )
    output_schema: typing.Dict[str, typing.Dict] = Field(
        description="The output schema for this module."
    )
    outputs: typing.Dict[str, typing.Any] = Field(
        description="The (dummy) output for this module.", default_factory=dict
    )
    delay: float = Field(
        description="The delay in seconds from processing start to when the (dummy) outputs are returned.",
        default=0,
    )


class DummyModule(KiaraModule):
    """Module that simulates processing, but uses hard-coded outputs as a result."""

    _config_cls = DummyProcessingModuleConfig

    def create_input_schema(self) -> typing.Mapping[str, ValueSchema]:
        """The input schema for the ``dummy`` module is created at object creation time from the ``input_schemas`` config parameter."""

        result = {}
        for k, v in self.config.get("input_schema").items():  # type: ignore
            schema = ValueSchema(**v)
            schema.validate_types(self._kiara)
            result[k] = schema
        return result

    def create_output_schema(self) -> typing.Mapping[str, ValueSchema]:
        """The output schema for the ``dummy`` module is created at object creation time from the ``output_schemas`` config parameter."""

        result = {}
        for k, v in self.config.get("output_schema").items():  # type: ignore
            schema = ValueSchema(**v)
            schema.validate_types(self._kiara)
            result[k] = schema
        return result

    def process(self, inputs: ValueSet, outputs: ValueSet) -> None:
        """Returns the hardcoded output values that are set in the ``outputs`` config field.

        Optionally, this module can simulate processing by waiting a configured amount of time (seconds -- specified in the ``delay`` config parameter).
        """

        time.sleep(self.config.get("delay"))  # type: ignore

        output_values: typing.Mapping = self.config.get("outputs")  # type: ignore

        value_dict = {}
        for output_name in self.output_names:
            if output_name not in output_values.keys():
                raise NotImplementedError()
                # v = self.output_schemas[output_name].type_obj.fake_value()
                # value_dict[output_name] = v
            else:
                value_dict[output_name] = output_values[output_name]
        outputs.set_values(**value_dict)

    # def _get_doc(self) -> str:
    #
    #     doc = self.config.get("doc", None)
    #
    #     if doc:
    #         return self.config["doc"]
    #     else:
    #         return super()._get_doc()
