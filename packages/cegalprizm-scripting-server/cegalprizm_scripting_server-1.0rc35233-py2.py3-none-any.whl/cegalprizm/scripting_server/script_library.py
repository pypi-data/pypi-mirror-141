# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

import sys
import traceback
from types import ModuleType
import hashlib
import sys
from io import StringIO
import contextlib

from . import logger

script_dict = {}


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@contextlib.contextmanager
def stderrIO(stderr=None):
    old = sys.stderr
    if stderr is None:
        stderr = StringIO()
    sys.stderr = stderr
    yield stderr
    sys.stderr = old


def compile_script(script, injected_vars, cache_module):
    try:
        function_id = hashlib.md5(script.encode('utf-8')).hexdigest()
        if function_id in script_dict.keys():
            logger.debug(f"Script already exists")
            return (True, function_id, "", "")

        try:
            logger.debug(f"Compiling script")

            code = f"{script}"

            if injected_vars is not None and len(injected_vars) > 0:
                injection_code = ""
                for key, value in injected_vars.items():
                    injection_code += f"{key} = {value}\n"
                code = f"{injection_code}\n{code}"

            logger.debug(code)
            compiled = compile(code, '', 'exec')
            module = ModuleType(function_id)

            with stdoutIO() as stdout:
                with stderrIO() as stderr:
                    try:
                        exec(compiled, module.__dict__)  # injected_vars
                    except Exception as error:
                        detail = error.args[0]
                        cl, exc, tb = sys.exc_info()
                        line_number = traceback.extract_tb(tb)[-1][1]
                        error_message = f"Exception running script: line {line_number}: {error}: {detail}"
                        logger.error(error_message)
                        return (False, error_message)

            if cache_module:
                script_dict[function_id] = module

            logger.debug(f"Script compiled")
            return (True, function_id, stdout.getvalue(), stderr.getvalue())
        except Exception as error:
            error_message = f"Exception compiling script: {type(error)}: {error}: {error.args}"
            logger.error(error_message)
            return (False, error_message)
    except:
        return (False, "Script not valid")


def get_module(function_id: str):
    if function_id not in script_dict.keys():
        return None
    
    return script_dict[function_id]
