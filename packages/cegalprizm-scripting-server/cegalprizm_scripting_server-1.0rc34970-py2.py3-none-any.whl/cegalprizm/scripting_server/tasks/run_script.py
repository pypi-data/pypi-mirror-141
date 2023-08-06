from typing import Tuple

from google.protobuf.any_pb2 import Any

from .. import logger
from ..script_library import compile_script
from ..script_parameters import get_value_from_payload
from ..scripting_server_pb2 import RunScriptRequest, ExecutionResponse


def RunScript(payload: Any) -> Tuple[bool, Any, str]:
    logger.info(f"Run script request")
    request = RunScriptRequest()
    payload.Unpack(request)

    injected_vars = None
    if request.injected_vars is not None:
        injected_vars = {}
        for item in request.injected_vars.dict.items():
            input = get_value_from_payload(item[1])
            if input[0]:
                if input[1] is not None:
                    injected_vars[item[0]] = input[1] 
        logger.debug(f"Injected : {injected_vars}")

    compile_result = compile_script(request.script, injected_vars, False)
    if not compile_result[0]:
        return (False, compile_result[1])

    result = ExecutionResponse()
    result.std_out = compile_result[2]
    result.std_err = compile_result[3]

    logger.info(f"Script executed successfully")
    return (True, result, "")
