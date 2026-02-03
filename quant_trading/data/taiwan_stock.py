"""
台股數據獲取模組
Taiwan Stock Data Fetcher
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaiwanStockFetcher:
    """
    台股數據獲取器
    使用 Yahoo Finance API 獲取台股數據
    """

    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}

    def get_stock_data(
        self,
        symbol: str,
        start_date: str = None,
        end_date: str = None,
        period: str = "2y"
    ) -> pd.DataFrame:
        """
        獲取單一股票歷史數據

        Args:
            symbol: 股票代碼 (例如 "2330.TW")
            start_date: 開始日期 (YYYY-MM-DD)
            end_date: 結束日期 (YYYY-MM-DD)
            period: 時間週期 (如果沒指定日期)

        Returns:
            包含 OHLCV 數據的 DataFrame
        """
        try:
            ticker = yf.Ticker(symbol)

            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)

            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()

            # 標準化欄位名稱
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })

            # 只保留需要的欄位
            columns_to_keep = ['open', 'high', 'low', 'close', 'volume']
            df = df[[col for col in columns_to_keep if col in df.columns]]

            df['symbol'] = symbol
            df.index = pd.to_datetime(df.index)
            df.index = df.index.tz_localize(None)  # 移除時區資訊

            logger.info(f"Fetched {len(df)} rows for {symbol}")
            return df

        except Exception as e:
            logger.error(f"Error fetching {symbol}: {e}")
            return pd.DataFrame()

    def get_multiple_stocks(
        self,
        symbols: List[str],
        start_date: str = None,
        end_date: str = None,
        period: str = "2y"
    ) -> Dict[str, pd.DataFrame]:
        """
        獲取多支股票數據

        Args:
            symbols: 股票代碼列表
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期

        Returns:
            以股票代碼為鍵的 DataFrame 字典
        """
        result = {}
        for symbol in symbols:
            df = self.get_stock_data(symbol, start_date, end_date, period)
            if not df.empty:
                result[symbol] = df
        return result

    def get_benchmark_data(
        self,
        benchmark: str = "0050.TW",
        start_date: str = None,
        end_date: str = None,
        period: str = "5y"
    ) -> pd.DataFrame:
        """
        獲取基準指數 (0050 ETF) 數據用於比較

        Args:
            benchmark: 基準 ETF 代碼
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期

        Returns:
            基準 ETF 的價格數據
        """
        return self.get_stock_data(benchmark, start_date, end_date, period)

    def calculate_returns(
        self,
        df: pd.DataFrame,
        column: str = 'close'
    ) -> pd.DataFrame:
        """
        計算報酬率

        Args:
            df: 價格數據
            column: 用於計算的價格欄位

        Returns:
            包含各種報酬率的 DataFrame
        """
        result = df.copy()

        # 日報酬率
        result['daily_return'] = result[column].pct_change()

        # 累積報酬率
        result['cumulative_return'] = (1 + result['daily_return']).cumprod() - 1

        # 對數報酬率 (用於統計分析)
        result['log_return'] = np.log(result[column] / result[column].shift(1))

        return result

    def get_combined_data(
        self,
        symbols: List[str],
        start_date: str = None,
        end_date: str = None,
        period: str = "2y"
    ) -> pd.DataFrame:
        """
        獲取多支股票的收盤價合併數據

        Args:
            symbols: 股票代碼列表
            start_date: 開始日期
            end_date: 結束日期
            period: 時間週期

        Returns:
            以日期為索引、股票代碼為欄位的收盤價 DataFrame
        """
        data = self.get_multiple_stocks(symbols, start_date, end_date, period)

        if not data:
            return pd.DataFrame()

        # 合併所有股票的收盤價
        close_prices = pd.DataFrame()
        for symbol, df in data.items():
            if 'close' in df.columns:
                close_prices[symbol] = df['close']

        return close_prices

    def get_market_cap_weights(self, symbols: List[str]) -> Dict[str, float]:
        """
        獲取市值權重 (用於加權計算)

        Args:
            symbols: 股票代碼列表

        Returns:
            市值權重字典
        """
        market_caps = {}

        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                market_cap = info.get('marketCap', 0)
                if market_cap:
                    market_caps[symbol] = market_cap
            except Exception as e:
                logger.warning(f"Could not get market cap for {symbol}: {e}")

        # 計算權重
        total = sum(market_caps.values())
        if total > 0:
            weights = {k: v / total for k, v in market_caps.items()}
        else:
            # 等權重
            weights = {s: 1/len(symbols) for s in symbols}

        return weights


def get_taiwan_etf_comparison() -> Dict[str, str]:
    """
    獲取常見台股 ETF 清單用於比較
    """
    return {
        "0050.TW": "元大台灣50",
        "0056.TW": "元大高股息",
        "006208.TW": "富邦台50",
        "00878.TW": "國泰永續高股息",
        "00713.TW": "元大台灣高息低波",
        "00850.TW": "元大臺灣ESG永續",
        "00692.TW": "富邦公司治理",
        "00881.TW": "國泰台灣5G+",
        "00891.TW": "中信關鍵半導體",
        "00900.TW": "富邦特選高股息30",
    }


# 使用範例
if __name__ == "__main__":
    fetcher = TaiwanStockFetcher()

    # 獲取台積電數據
    tsmc = fetcher.get_stock_data("2330.TW", period="1y")
    print(f"台積電數據筆數: {len(tsmc)}")

    # 計算報酬率
    tsmc_returns = fetcher.calculate_returns(tsmc)
    print(f"台積電年化報酬率: {tsmc_returns['daily_return'].mean() * 252:.2%}")
