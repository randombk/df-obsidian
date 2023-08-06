#
# Based on alef's implementation at http://www.bay12forums.com/smf/index.php?topic=178089
#
import sys
import asyncio
from enum import IntEnum
from pathlib import Path

# Append 'dfhack_proto' to the path so we can import the protobuf messages
sys.path.append(str(Path(__file__).parent / 'dfhack_proto'))

import dfhack_proto.CoreProtocol_pb2 as CoreProtocol_pb2
from dfhack_proto.CoreProtocol_pb2 import EmptyMessage, StringMessage

_reader, _writer = None, None


class DFHackReplyCode(IntEnum):
    RPC_REPLY_RESULT = -1
    RPC_REPLY_FAIL   = -2
    RPC_REPLY_TEXT   = -3
    RPC_REQUEST_QUIT = -4


def header(id, size):
    return id.to_bytes(2, sys.byteorder, signed=True) + b'\x00\x00' + size.to_bytes(4, sys.byteorder)


async def get_header():
    h = await _reader.read(8)
    id = int.from_bytes(h[0:2], sys.byteorder, signed=True)
    size = int.from_bytes(h[4:7], sys.byteorder)
    return id, size


def request(id, msg):
    s = msg.SerializeToString()
    h = header(id, len(s))
    return h + s


async def parse_response(outputType):
    id, size = await get_header()

    if id == DFHackReplyCode.RPC_REPLY_RESULT:
        buffer = await _reader.read(size)
        size -= len(buffer)
        while size:
            more = await _reader.read(size)
            buffer += more
            size -= len(more)
        obj = outputType()
        obj.ParseFromString(buffer)
        return obj
    elif id == DFHackReplyCode.RPC_REPLY_TEXT:
        msg = await _reader.read(size)
        obj = CoreProtocol_pb2.CoreTextNotification()
        obj.ParseFromString(msg)
        raise Exception(obj)
    else:
        raise Exception(f"Unknown reply code {id}")


binding_cache = {}
async def BindMethod(method, inputType, outputType, plugin=''):
    """Issue a CoreBindRequest to DFHack and caches the returned identifier number
    """
    if (method, inputType, outputType, plugin) in binding_cache:
        return binding_cache[(method, inputType, outputType, plugin)]
    else:
        br = CoreProtocol_pb2.CoreBindRequest()
        br.method, br.input_msg, br.output_msg, br.plugin = \
            method, inputType.DESCRIPTOR.full_name, outputType.DESCRIPTOR.full_name, plugin
        _writer.write(request(0, br))

        result = (await parse_response(CoreProtocol_pb2.CoreBindReply)).assigned_id
        binding_cache[(method, inputType, outputType, plugin)] = result
        return result


def handshake_request():
    n = 1
    return b'DFHack?\n' + n.to_bytes(4, sys.byteorder, signed=False)


async def connect(host='127.0.0.1', port=5000):
    global _reader, _writer
    _reader, _writer = await asyncio.open_connection(host, port)
    _writer.write( handshake_request() )
    msg = await _reader.read(12)
    if b'DFHack!\n\x01\x00\x00\x00' != msg:  # handshake_reply
        _reader, _writer = None, None


async def close():
    buf = header(DFHackReplyCode.RPC_REQUEST_QUIT, 0) + b'\x00\x00\x00\x00'
    if _writer is not None:
        _writer.write(buf) ; await _writer.drain()
        _writer.close() ; await _writer.wait_closed()


def remote(plugin=''):
    """ Decorator that uses type annotations to bind DFHack Remote functions

    Example:
    @remote(plugin='RemoteFortressReader')
    async def GetVersionInfo(input: EmptyMessage = None, output: VersionInfo = None):

    @remote
    async def GetVersion(output: StringMessage = None):
    """

    from functools import update_wrapper
    from inspect import signature
    inputType, outputType, function, _plugin = None, None, None, None

    async def wrapper(requestData = None):
        reqID = await BindMethod(function.__name__, inputType, outputType, _plugin)
        _writer.write(request(reqID, requestData or inputType()))
        return await parse_response(outputType)

    def parse(f):
        nonlocal inputType, outputType, function
        function = f
        p = signature(f).parameters
        try:
            inputType = p['input'].annotation
        except KeyError:
            inputType = EmptyMessage
        outputType = p['output'].annotation
        return update_wrapper(wrapper, f)

    # For ease of writing signatures, let's use 'plugin' also for plain decorator
    if isinstance(plugin, str):  # The plugin name
        _plugin = plugin
        return parse
    else:
        _plugin = ''
        return parse(plugin)  # The decorated function
