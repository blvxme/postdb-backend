from asyncio import to_thread
from json import dumps
from typing import Any


async def build_output_message(local_output: dict[str, Any], global_output: dict[str, Any]) -> str:
    process_name = ""
    if "self" in local_output:
        self_object = local_output["self"]
        cls = self_object.__class__
        class_name = cls.__name__
        process_name = class_name

    process_states = {}
    if "pStates" in global_output:
        process_states = {k.removesuffix("_state"): v for k, v in global_output["pStates"].items()}

    input_variables = {}
    if "inVars" in global_output:
        input_variables = global_output["inVars"]

    output_variables = {}
    if "outVars" in global_output:
        output_variables = global_output["outVars"]

    return await to_thread(
        dumps,
        {
            "process_name": process_name,
            "process_states": process_states,
            "input_variables": input_variables,
            "output_variables": output_variables,
        },
        default=str
    )
