import asyncio
from typing import Iterable

import httpx

from src.hyper_liquid import HyperLiquid, InvalidUserAddress
from src.trades import Trade, get_completed_perpetual_trades


async def main():
    user = input("Enter HyperLiquid user address: ").strip()

    print("Fetching trade history ...\n")
    async with httpx.AsyncClient() as client:
        hyper_liquid = HyperLiquid(client)
        try:
            fills = await hyper_liquid.get_user_fills(user)
        except InvalidUserAddress:
            print(f"Invalid user address: {user}")
            print(
                "Example of valid user address: 0x63cdc4b2e50a4e51451c5ca6e494c0e96e8f2d37"
            )
            return

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
