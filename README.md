# Market Values

Live Indian stock market tracker with a web dashboard. Tracks NSE stocks in real-time using WebSocket streaming, with candlestick charts and a clean UI.

## Install

```bash
pip install market-values
```

## Usage

```bash
market-values              # starts server and opens browser
market-values --port 9000  # custom port
market-values --no-browser # don't auto-open browser
```

The dashboard will be available at `http://127.0.0.1:8000` (default).

## Configuration

On first run, a config file is created at `~/.market-values/config.yaml`:

```yaml
stock_codes:
- RELIANCE.NS
- TCS.NS
- INFY.NS
- HDFCBANK.NS
- ICICIBANK.NS
server:
  host: 127.0.0.1
  port: 8000
refresh_interval_seconds: 5
```

Edit the stock codes to track different NSE stocks. Changes are picked up automatically without restarting.

## License

MIT
