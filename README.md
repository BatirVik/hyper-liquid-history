# HyperLiquid Perp Trade History Test

## Instructions

This script fetches and displays the completed perp trade history of a given HyperLiquid user address.

### Usage

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the script:
```
python main.py
```

3. When prompted, enter the wallet address.

### Output

The script will display a list of completed perp trades including:
- Coin
- Direction (Long/Short)
- Entry time
- Duration of the position
- Realized PnL (USD)

### Notes

- Public API access (no authentication required)
- Refer to https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint
