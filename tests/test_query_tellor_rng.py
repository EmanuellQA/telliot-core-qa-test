""" Unit tests for Tellor RNG Query

Copyright (c) 2022-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from eth_abi import decode_abi
from eth_abi import decode_single

from telliot_core.queries.tellor_rng import TellorRNG


def test_tellor_rng_query():
    """Validate tellor rng query"""
    q = TellorRNG(
        timestamp=1000000,
    )
    assert q.value_type.abi_type == "bytes32"
    assert q.value_type.packed is False

    print(q.query_data)
    exp_abi = (
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x54\x65\x6c\x6c\x6f\x72"
        b"\x52\x4e\x47\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x0f\x42\x40"
    )

    assert q.query_data == exp_abi

    query_type, encoded_param_vals = decode_abi(["string", "bytes"], q.query_data)
    assert query_type == "TellorRNG"

    timestamp = decode_single("uint256", encoded_param_vals)

    assert timestamp == 1000000
    assert isinstance(timestamp, int)
    assert q.query_id.hex() == "3f43c74ef29e7115b1788f887bcd92a88a242fbab13e1721339adf7b238a473b"
