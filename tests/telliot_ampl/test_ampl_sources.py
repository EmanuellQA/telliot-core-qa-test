import os
from datetime import datetime

import pytest

from telliot_ampl.config import AMPLConfig
from telliot_ampl.sources import AnyBlockSource
from telliot_ampl.sources import BraveNewCoinSource


@pytest.fixture
def cfg():
    c = AMPLConfig()

    if not c.main.anyblock_api_key:
        c.main.anyblock_api_key = os.environ["ANYBLOCK_KEY"]

    if not c.main.rapid_api_key:
        c.main.rapid_api_key = os.environ["RAPID_KEY"]

    return c


@pytest.mark.asyncio
async def test_bravenewcoin_source(cfg):
    """Test retrieving AMPL/USD/VWAP data from BraveNewCoin/Rapid api.

    Retrieves bearer token and adds to headers of main data request."""

    api_key = cfg.main.rapid_api_key
    ampl_source = BraveNewCoinSource()

    datapoint, status = await ampl_source.fetch_new_datapoint(api_key)
    value, timestamp = datapoint

    assert status.ok
    assert isinstance(value, float)
    assert isinstance(timestamp, datetime)
    assert value > 0


@pytest.mark.asyncio
async def test_anyblock_source(cfg):
    """Test retrieving AMPL/USD/VWAP data from AnyBlock api."""

    api_key = cfg.main.anyblock_api_key
    ampl_source = AnyBlockSource()

    datapoint, status = await ampl_source.fetch_new_datapoint(api_key)
    value, timestamp = datapoint

    assert status.ok
    assert isinstance(value, float)
    assert isinstance(timestamp, datetime)
    assert value > 0
