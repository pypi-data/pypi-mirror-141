from typing import Tuple

from google.protobuf.any_pb2 import Any

from .. import logger
from ..script_library import compile_script
from ..scripting_server_pb2 import CreateFunctionRequest, CreateFunctionResponse


def CreateFunction(payload) -> Tuple[bool, Any, str]:
    logger.info(f"Create function request")
    request = CreateFunctionRequest()
    payload.Unpack(request)

    if len(request.script) > 0:
        logger.debug(f"Using script")
        script = request.script
    elif len(request.pickled_object) > 0:
        logger.debug(f"Using pickled_object")
        script = f"""
import cloudpickle
import base64
pyFunc = cloudpickle.loads(base64.b64decode('{request.pickled_object}'))
        """
    else:
        return (False, "Cannot create function")

    compile_result = compile_script(script, None, True)
    if not compile_result[0]:
        return (False, compile_result[1])

    function_id = compile_result[1]
    logger.info(f"Function cached with id {function_id}")
    result = CreateFunctionResponse()
    result.function_id = function_id

    return (True, result, "")
