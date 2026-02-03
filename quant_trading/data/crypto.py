"""
加密貨幣數據獲取模組
Cryptocurrency Data Fetcher
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False

import yfinance as yf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CryptoFetcher:
    """
    加密貨幣數據獲取器
    支援 CCXT (多交易所) 和 Yahoo Finance 作為備用
    """

    def __init__(self, exchange_id: str = "binance"):
        """
        初始化加密貨幣獲取器

        Args:
            exchange_id: 交易所 ID (binance, coinbase, kraken 等)
        """
        self.exchange_id = exchange_id
        self.exchange = None

        if CCXT_AVAILABLE:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.exchange = exchange_class({
                    'enableRateLimit': True,
                    'options': {'defaultType': 'spot'}
                })
                logger.info(f"Connected to {exchange_id} via CCXT")
            except Exception as e:
                logger.warning(f"Failed to initialize CCXT for {exchange_id}: {e}")
        else:
            logger.warning("CCXT not available, using Yahoo Finance as fallback")

        # Yahoo Finance 符號對應
        self.yf_symbol_map = {
            "BTC/USDT": "BTC-USD",
            "ETH/USDT": "ETH-USD",
            "BNB/USDT": "BNB-USD",
            "SOL/USDT": "SOL-USD",
            "XRP/USDT": "XRP-USD",
            "ADA/USDT": "ADA-USD",
            "AVAX/USDT": "AVAX-USD",
            "DOT/USDT": "DOT-USD",
            "MATIC/USDT": "MATIC-USD",
            "LINK/USDT": "LINK-USD",
            "DOGE/USDT": "DOGE-USD",
            "ATOM/USDT": "ATOM-USD",
            "UNI/USDT": "UNI-USD",
            "LTC/USDT": "LTC-USD",
        }

    def get_ohlcv_ccxt(
        self,
        symbol: str,
        timeframe: str = "1d",
        since: int = None,
        limit: int = 1000
    ) -> pd.DataFrame:
        """
        使用 CCXT 獲取 OHLCV 數據

        Args:
            symbol: 交易對 (例如 "BTC/USDT")
            timeframe: 時間框架 (1m, 5m, 1h, 1d 等)
            since: 開始時間戳 (毫秒)
            limit: 數據筆數限制

        Returns:
            OHLCV DataFrame
        """
        if not self.exchange:
            return pd.DataFrame()

        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)

            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )

            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df['symbol'] = symbol

            logger.info(f"Fetched {len(df)} rows for {symbol} from {self.exchange_id}")
            return df

        except Exception as e:
            logger.error(f"CCXT error fetching {symbol}: {e}")
            return pd.DataFrame()

    def get_ohlcv_yfinance(
        self,
        symbol: str,
        start_date: str = None,
        end_date: str = None,
        period: str = "2y"
    ) -> pd.DataFrame:
        """
        使用 Yahoo Finance 獲取 OHLCV 數據 (備用方案)

        Args:
            symbol: 交易對 (例如 "BTC/USDT")
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期

        Returns:
            OHLCV DataFrame
        """
        yf_symbol = self.yf_symbol_map.get(symbol, symbol.replace("/", "-"))

        try:
            ticker = yf.Ticker(yf_symbol)

            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)

            if df.empty:
                logger.warning(f"No data found for {symbol} ({yf_symbol})")
                return pd.DataFrame()

            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })

            columns_to_keep = ['open', 'high', 'low', 'close', 'volume']
            df = df[[col for col in columns_to_keep if col in df.columns]]

            df['symbol'] = symbol
            df.index = pd.to_datetime(df.index)
            df.index = df.index.tz_localize(None)

            logger.info(f"Fetched {len(df)} rows for {symbol} from Yahoo Finance")
            return df

        except Exception as e:
            logger.error(f"Yahoo Finance error fetching {symbol}: {e}")
            return pd.DataFrame()

    def get_crypto_data(
        self,
        symbol: str,
        start_date: str = None,
        end_date: str = None,
        period: str = "2y",
        timeframe: str = "1d"
    ) -> pd.DataFrame:
        """
        獲取加密貨幣數據 (自動選擇數據源)

        Args:
            symbol: 交易對
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期
            timeframe: CCXT 時間框架

        Returns:
            OHLCV DataFrame
        """
        # 優先使用 CCXT
        if self.exchange and CCXT_AVAILABLE:
            if start_date:
                since = int(pd.Timestamp(start_date).timestamp() * 1000)
            else:
                # 預設獲取 2 年數據
                since = int((datetime.now() - timedelta(days=730)).timestamp() * 1000)

            df = self.get_ohlcv_ccxt(symbol, timeframe, since)
            if not df.empty:
                return df

        # 回退到 Yahoo Finance
        return self.get_ohlcv_yfinance(symbol, start_date, end_date, period)

    def get_multiple_cryptos(
        self,
        symbols: List[str],
        start_date: str = None,
        end_date: str = None,
        period: str = "2y"
    ) -> Dict[str, pd.DataFrame]:
        """
        獲取多個加密貨幣數據

        Args:
            symbols: 交易對列表
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期

        Returns:
            以交易對為鍵的 DataFrame 字典
        """
        result = {}
        for symbol in symbols:
            df = self.get_crypto_data(symbol, start_date, end_date, period)
            if not df.empty:
                result[symbol] = df
        return result

    def get_combined_data(
        self,
        symbols: List[str],
        start_date: str = None,
        end_date: str = None,
        period: str = "2y"
    ) -> pd.DataFrame:
        """
        獲取多個加密貨幣的收盤價合併數據

        Args:
            symbols: 交易對列表
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期

        Returns:
            以日期為索引的收盤價 DataFrame
        """
        data = self.get_multiple_cryptos(symbols, start_date, end_date, period)

        if not data:
            return pd.DataFrame()

        close_prices = pd.DataFrame()
        for symbol, df in data.items():
            if 'close' in df.columns:
                close_prices[symbol] = df['close']

        return close_prices

    def calculate_returns(self, df: pd.DataFrame, column: str = 'close') -> pd.DataFrame:
        """
        計算報酬率

        Args:
            df: 價格數據
            column: 用於計算的價格欄位

        Returns:
            包含報酬率的 DataFrame
        """
        result = df.copy()

        result['daily_return'] = result[column].pct_change()
        result['cumulative_return'] = (1 + result['daily_return']).cumprod() - 1
        result['log_return'] = np.log(result[column] / result[column].shift(1))

        return result

    def get_fear_greed_index(self) -> Dict:
        """
        獲取加密貨幣恐懼貪婪指數 (可選功能)
        """
        try:
            import requests
            response = requests.get(
                "https://api.alternative.me/fng/",
                timeout=10
            )
            data = response.json()
            if 'data' in data:
                return {
                    'value': int(data['data'][0]['value']),
                    'classification': data['data'][0]['value_classification'],
                    'timestamp': data['data'][0]['timestamp']
                }
        except Exception as e:
            logger.warning(f"Failed to fetch Fear & Greed Index: {e}")

        return {}


def get_major_cryptos() -> List[str]:
    """
    獲取主要加密貨幣清單
    """
    return [
        "BTC/USDT",
        "ETH/USDT",
        "BNB/USDT",
        "SOL/USDT",
        "XRP/USDT",
        "ADA/USDT",
        "AVAX/USDT",
        "DOT/USDT",
        "MATIC/USDT",
        "LINK/USDT",
    ]


# 使用範例
if __name__ == "__main__":
    fetcher = CryptoFetcher()

    # 獲取比特幣數據
    btc = fetcher.get_crypto_data("BTC/USDT", period="1y")
    print(f"比特幣數據筆數: {len(btc)}")

    if not btc.empty:
        btc_returns = fetcher.calculate_returns(btc)
        print(f"比特幣年化報酬率: {btc_returns['daily_return'].mean() * 365:.2%}")
        print(f"比特幣年化波動率: {btc_returns['daily_return'].std() * np.sqrt(365):.2%}")
