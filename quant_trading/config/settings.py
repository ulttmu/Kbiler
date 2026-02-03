"""
量化交易系統配置
Quantitative Trading System Configuration
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class TaiwanStockConfig:
    """台股配置"""
    # 主要追蹤的 ETF 和股票代碼
    benchmark_etf: str = "0050.TW"  # 台灣50 ETF (用於比較)
    benchmark_etf_2: str = "0056.TW"  # 高股息 ETF

    # 追蹤的台股清單 (可自行擴充)
    watchlist: List[str] = None

    # 交易時間
    market_open: str = "09:00"
    market_close: str = "13:30"

    # 手續費與稅率
    commission_rate: float = 0.001425  # 券商手續費 0.1425%
    tax_rate: float = 0.003  # 證交稅 0.3%

    def __post_init__(self):
        if self.watchlist is None:
            self.watchlist = [
                "2330.TW",  # 台積電
                "2317.TW",  # 鴻海
                "2454.TW",  # 聯發科
                "2308.TW",  # 台達電
                "2881.TW",  # 富邦金
                "2882.TW",  # 國泰金
                "2412.TW",  # 中華電
                "3008.TW",  # 大立光
                "2303.TW",  # 聯電
                "1301.TW",  # 台塑
            ]


@dataclass
class CryptoConfig:
    """加密貨幣配置"""
    # 交易所
    exchange: str = "binance"

    # 追蹤的加密貨幣對
    watchlist: List[str] = None

    # 交易費用
    maker_fee: float = 0.001  # 0.1%
    taker_fee: float = 0.001  # 0.1%

    def __post_init__(self):
        if self.watchlist is None:
            self.watchlist = [
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


@dataclass
class BacktestConfig:
    """回測配置"""
    # 回測期間
    start_date: str = "2020-01-01"
    end_date: str = None  # None 表示到今天

    # 初始資金
    initial_capital: float = 1_000_000  # 100萬

    # 風險管理
    max_position_size: float = 0.2  # 單一標的最大部位 20%
    stop_loss_pct: float = 0.08  # 停損 8%
    take_profit_pct: float = 0.25  # 停利 25%

    # 再平衡頻率
    rebalance_frequency: str = "monthly"  # daily, weekly, monthly, quarterly

    def __post_init__(self):
        if self.end_date is None:
            self.end_date = datetime.now().strftime("%Y-%m-%d")


@dataclass
class PortfolioConfig:
    """投資組合配置"""
    # 資產類別配置
    asset_allocation: Dict[str, float] = None

    # 風險偏好: conservative, moderate, aggressive
    risk_profile: str = "moderate"

    # 目標年化報酬率
    target_return: float = 0.12  # 12%

    # 最大可接受波動率
    max_volatility: float = 0.20  # 20%

    def __post_init__(self):
        if self.asset_allocation is None:
            # 預設配置
            allocations = {
                "conservative": {
                    "taiwan_stocks": 0.30,
                    "crypto": 0.05,
                    "cash": 0.65
                },
                "moderate": {
                    "taiwan_stocks": 0.50,
                    "crypto": 0.15,
                    "cash": 0.35
                },
                "aggressive": {
                    "taiwan_stocks": 0.60,
                    "crypto": 0.30,
                    "cash": 0.10
                }
            }
            self.asset_allocation = allocations.get(self.risk_profile, allocations["moderate"])


# 全局配置實例
TAIWAN_CONFIG = TaiwanStockConfig()
CRYPTO_CONFIG = CryptoConfig()
BACKTEST_CONFIG = BacktestConfig()
PORTFOLIO_CONFIG = PortfolioConfig()
