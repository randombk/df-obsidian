cmake_minimum_required(VERSION 3.13)
project(df-obsidian NONE)

set(PROTOC_BIN "protoc")
set(DFHACK_DIR        "${CMAKE_CURRENT_SOURCE_DIR}/dfhack")
set(PROTO_OUTPUT_DIR  "${CMAKE_CURRENT_BINARY_DIR}/dfhack_proto")

add_custom_command(OUTPUT protos
    COMMAND git submodule update --init --recursive
    COMMAND mkdir -p ${PROTO_OUTPUT_DIR}
    COMMAND touch ${PROTO_OUTPUT_DIR}/__init__.py
    COMMAND "${PROTOC_BIN}"
    -I${DFHACK_DIR}/library/proto
    -I${DFHACK_DIR}/plugins/remotefortressreader/proto
    --python_out=${PROTO_OUTPUT_DIR}
    ${DFHACK_DIR}/plugins/remotefortressreader/proto/RemoteFortressReader.proto
    ${DFHACK_DIR}/plugins/remotefortressreader/proto/ItemdefInstrument.proto
    ${DFHACK_DIR}/library/proto/CoreProtocol.proto
    ${DFHACK_DIR}/library/proto/Basic.proto
    ${DFHACK_DIR}/library/proto/BasicApi.proto
)

add_custom_target(DONE ALL
  DEPENDS protos
)
