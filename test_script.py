import httpx
import pytest

from hyper_liquid import HyperLiquid
from utils import split_time_window


def test_split_time_window():
    assert split_time_window((100, 200)) == ((100, 150), (151, 200))
    assert split_time_window((1, 4)) == ((1, 2), (3, 4))
    assert split_time_window((1, 5)) == ((1, 3), (4, 5))

    with pytest.raises(ValueError):
        split_time_window((1, 0))

    with pytest.raises(ValueError):
        split_time_window((1, 3))


@pytest.fixture
async def hyper():
    async with httpx.AsyncClient() as client:
        yield HyperLiquid(client)


TEST_USER = "0x63cdc4b2e50a4e51451c5ca6e494c0e96e8f2d37"


async def test_hyper_liquid_get_user_fills(hyper: HyperLiquid):
    fills = await hyper.get_user_fills(TEST_USER)

    assert len(fills) == len(set(f["tid"] for f in fills)), "duplicates"

    times = [f["time"] for f in fills]
    times_sorted = list(sorted(times))
    assert times == times_sorted, "sorted"
