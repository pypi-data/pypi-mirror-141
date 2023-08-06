# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from cegalprizm.hub import HubTaskRegistry

from .tasks.run_script import RunScript
from .tasks.create_function import CreateFunction
from .tasks.execute_function import ExecuteFunction


def get_task_registry() -> HubTaskRegistry:

    registry = HubTaskRegistry()

    registry.register_unary_task(wellknown_payload_identifier="cegal.scripting_server.run_script",
                                 task=RunScript,
                                 friendly_name="Run script",
                                 description="Runs a script",
                                 payload_auth=None)

    registry.register_unary_task(wellknown_payload_identifier="cegal.scripting_server.create_function",
                                 task=CreateFunction,
                                 friendly_name="Create function",
                                 description="Compiles the supplied script so that it can be executed as a function",
                                 payload_auth=None)

    registry.register_unary_task(wellknown_payload_identifier="cegal.scripting_server.execute_function",
                                 task=ExecuteFunction,
                                 friendly_name="Execute function",
                                 description="Executes a function with the supplied parameters and returns the result",
                                 payload_auth=None)

    return registry
