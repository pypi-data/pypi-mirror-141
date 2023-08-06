# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from .scripting_server_pb2 import DoubleValuePayload, Double1DPayload, Double2DPayload
from .scripting_server_pb2 import IntValuePayload, Int1DPayload, Int2DPayload
from .scripting_server_pb2 import BoolValuePayload, Bool1DPayload
from .scripting_server_pb2 import StringValuePayload, String1DPayload


def get_value_from_payload(parameter):
    if parameter is None:
        return (False, None)

    if parameter.content_type == "DoubleValuePayload":
        input = DoubleValuePayload()
        parameter.content.Unpack(input)
        return (True, input.value)
    elif parameter.content_type == "Double1DPayload":
        input = Double1DPayload()
        parameter.content.Unpack(input)
        return (True, [x for x in input.values])
    elif parameter.content_type == "Double2DPayload":
        input = Double2DPayload()
        parameter.content.Unpack(input)
        val = []
        for x in input.values:
            val.append([y for y in x.values])
        return (True, val)
    elif parameter.content_type == "IntValuePayload":
        input = IntValuePayload()
        parameter.content.Unpack(input)
        return (True, input.value)
    elif parameter.content_type == "Int1DPayload":
        input = Int1DPayload()
        parameter.content.Unpack(input)
        return (True, [x for x in input.values])
    elif parameter.content_type == "Int2DPayload":
        input = Int2DPayload()
        parameter.content.Unpack(input)
        val = []
        for x in input.values:
            val.append([y for y in x.values])
        return (True, val)
    elif parameter.content_type == "BoolValuePayload":
        input = BoolValuePayload()
        parameter.content.Unpack(input)
        return (True, input.value)
    elif parameter.content_type == "Bool1DPayload":
        input = Bool1DPayload()
        parameter.content.Unpack(input)
        return (True, [x for x in input.values])
    elif parameter.content_type == "StringValuePayload":
        input = StringValuePayload()
        parameter.content.Unpack(input)
        return (True, input.value)
    elif parameter.content_type == "String1DPayload":
        input = String1DPayload()
        parameter.content.Unpack(input)
        return (True, [x for x in input.values])
    else:
        return (False, None)


def get_payload(payload_type: str, values):
    if payload_type == "DoubleValuePayload":
        output = DoubleValuePayload()
        output.value = values
        return (True, output)
    elif payload_type == "Double1DPayload":
        output = Double1DPayload()
        for x in values:
            output.values.append(x)
        return (True, output)
    elif payload_type == "Double2DPayload":
        output = Double2DPayload()
        for x in values:
            inner = Double1DPayload()
            for y in x.values:
                inner.append(y)
            output.values.append(inner)
        return (True, output)
    else:
        return (False, None)
