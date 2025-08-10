from datetime import datetime
from typing import Iterable, Literal, TypedDict


class Trade(TypedDict):
    direction: Literal["short", "long"]
    opened_at: datetime
    closed_at: datetime
    coin: str
    realized_pnl_usd: float


class OpenPosition(TypedDict):
    open_time: datetime
    direction: Literal["short", "long"]
    open_fill: dict
    status: str


def convert_pnl_to_usd(pnl_amount: float, fill_price: float, coin: str) -> float:
    if coin in ["USDC", "USDT", "USD"]:
        return pnl_amount
    return pnl_amount * fill_price


def get_completed_perpetual_trades(fills: Iterable) -> list[Trade]:  # ai generated
    coin_positions: dict[str, list[OpenPosition]] = {}
    completed_trades: list[Trade] = []

    for fill in fills:
        coin = str(fill.get("coin", "Unknown"))

        if coin.startswith("@"):
            continue

        side = str(fill.get("side", "Unknown"))
        time = datetime.fromtimestamp(fill.get("time", 0) / 1000)
        closed_pnl = float(fill.get("closedPnl", 0.0))
        start_position = float(fill.get("startPosition", 0.0))
        fill_price: float = float(fill.get("px", 0.0))
        fill_size = float(fill.get("sz", 0.0))

        # Calculate end position
        if side == "B":  # Buy
            end_position = start_position + fill_size
        else:  # side == "A" (Sell)
            end_position = start_position - fill_size

        # Initialize tracking for this coin if first time seeing it
        if coin not in coin_positions:
            coin_positions[coin] = []

        # Check for position state changes
        if start_position == 0 and end_position != 0:
            # Opening new position
            direction = "long" if end_position > 0 else "short"
            coin_positions[coin].append(
                {
                    "open_time": time,
                    "direction": direction,
                    "open_fill": fill,
                    "status": "open",
                }
            )

        elif start_position != 0 and end_position == 0:
            # Closing position - find the most recent open position
            for pos in reversed(coin_positions[coin]):
                if pos["status"] == "open":
                    completed_trades.append(
                        {
                            "coin": coin,
                            "direction": pos["direction"],
                            "opened_at": pos["open_time"],
                            "closed_at": time,
                            "realized_pnl_usd": convert_pnl_to_usd(
                                closed_pnl, fill_price, coin
                            ),
                        }
                    )
                    pos["status"] = "closed"
                    break

        # Handle position flips (long to short or short to long)
        elif (start_position > 0 and end_position < 0) or (
            start_position < 0 and end_position > 0
        ):
            for pos in reversed(coin_positions[coin]):
                if pos["status"] == "open":
                    completed_trades.append(
                        {
                            "coin": coin,
                            "direction": pos["direction"],
                            "opened_at": pos["open_time"],
                            "closed_at": time,
                            "realized_pnl_usd": convert_pnl_to_usd(
                                closed_pnl, fill_price, coin
                            ),
                        }
                    )
                    pos["status"] = "closed"
                    break

            # Open new position in opposite direction
            new_direction = "long" if end_position > 0 else "short"
            coin_positions[coin].append(
                {
                    "open_time": time,
                    "direction": new_direction,
                    "open_fill": fill,
                    "status": "open",
                }
            )

    open_positions = {}
    for coin, positions in coin_positions.items():
        for pos in positions:
            if pos["status"] == "open":
                open_positions[coin] = pos

    # if open_positions:
    #     print("Warning: The following positions are still open:")
    #     for coin, position in open_positions.items():
    #         print(
    #             f"Coin: {coin}, Direction: {position['direction'].upper()}, Open Time: {position['open_time']}"
    #         )

    return completed_trades
