from typing import Tuple

from google.protobuf.any_pb2 import Any

import sys
import traceback
from inspect import getmembers, isfunction

from .. import logger
from ..script_library import get_module
from ..script_parameters import get_value_from_payload, get_payload
from ..scripting_server_pb2 import ExecutionRequest, ExecutionResponse


def ExecuteFunction(payload) -> Tuple[bool, Any, str]:
    logger.info(f"Execute function request")
    request = ExecutionRequest()
    payload.Unpack(request)

    module = get_module(request.function_id)
    if not module:
        return (False, "Function has not been created")

    functions = getmembers(module, isfunction)
    logger.debug(functions)
    if len(functions) == 0:
        return (False, "No runnable function found")

    for fn_index, val in enumerate(functions):
        if val[0] not in request.function_names_to_ignore:
            break

    fn = functions[fn_index][1]

    try:
        input = get_value_from_payload(request.parameter)
        if input[0]:
            if input[1] is None:
                return (True, f"input_payload_type {request.input_payload_type} not recognised")
            else:
                input_values = input[1]
    except:
        return (False, "Exception parsing parameter")

    if input_values is not None:
        logger.debug(f"Input Type  : {request.parameter.content_type}")
        logger.debug(f"Input Values: {input_values}")

        try:
            output_values = fn(input_values)
        except Exception as error:
            detail = error.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            error_message = f"Exception running function: line {line_number}: {error}: {detail}"
            logger.error(error_message)
            return (False, error_message)

        try:
            logger.debug(f"Output Type  : {request.output_payload_type}")
            logger.debug(f"Output Values: {output_values}")

            output = get_payload(request.output_payload_type, output_values)
            if not output[0]:
                return (False, f"output_payload_type {request.output_payload_type} not recognised")
        except Exception as error:
            logger.error(error)
            return (False, "function results not of expected type")

    result = ExecutionResponse()
    result.output_payload.content_type = request.output_payload_type
    result.output_payload.content.Pack(output[1])

    logger.info(f"Function executed successfully")

    return (True, result, "")
