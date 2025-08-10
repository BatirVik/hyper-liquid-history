import asyncio
from typing import Iterable

import httpx

from src.hyper_liquid import HyperLiquid
from src.trades import Trade, get_completed_perpetual_trades


async def main():
    user = input("Enter HyperLiquid user address: ").strip()

    print("Fetching trade history ...\n")
    async with httpx.AsyncClient() as client:
        hyper_liquid = HyperLiquid(client)
        fills = await hyper_liquid.get_user_fills(user)

    trades = get_completed_perpetual_trades(fills)
    display_trades(trades)


def display_trades(trades: Iterable[Trade]) -> None:
    for trade in trades:
        duration = trade["closed_at"] - trade["opened_at"]
        print(
            f"Coin: {trade['coin']}",
            f"Direction: {trade['direction']}",
            f"Date opened: {trade['opened_at']}",
            f"Duration: {duration}",
            f"Realized PnL: {trade['realized_pnl_usd']:.2f}$",
            sep="\n",
            end="\n\n",
        )


if __name__ == "__main__":
    asyncio.run(main())
