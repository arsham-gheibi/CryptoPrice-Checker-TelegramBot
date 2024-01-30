from urllib.parse import urljoin


# Base Endpoints
BINANCE_BASE_ENDPOINT = 'https://api.binance.com'
KUCOIN_BASE_ENDPOINT = 'https://api.kucoin.com'
BYBIT_BASE_ENDPOINT = 'https://api.bybit.com'
BINGX_BASE_ENDPOINT = 'https://open-api.bingx.com'


# Endpoints
# Binance
BINANCE_SYMBOL_PRICE_TICKER = urljoin(
    BINANCE_BASE_ENDPOINT, '/api/v3/ticker/price'
)

# Kucoin
KUCOIN_SYMBOL_PRICE_TICKER = urljoin(
    KUCOIN_BASE_ENDPOINT, '/api/v1/market/orderbook/level1'
)

# Bybit
BYBIT_SYMBOL_PRICE_TICKER = urljoin(
    BYBIT_BASE_ENDPOINT, '/v5/market/tickers'
)

# BingX
BINGX_SYMBOL_PRICE_TICKER = urljoin(
    BINGX_BASE_ENDPOINT, '/openApi/spot/v1/ticker/24hr'
)
