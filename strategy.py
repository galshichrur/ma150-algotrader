"""
Core trading strategy implementation
"""

import pandas as pd
from config import STRATEGY_CONFIG

class TradingStrategy:
    """Implements 150MA trading logic"""

    def __init__(self):
        self.config = STRATEGY_CONFIG

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate buy/sell signals based on price-MA relationship"""
        df = df.copy()
        df['pct_diff'] = (df.price - df.ma) / df.ma

        # Buy signals
        df['buy'] = (
            (df.price > df.ma) &
            (df.pct_diff >= self.config['buy_threshold'][0]) &
            (df.pct_diff <= self.config['buy_threshold'][1])
        )

        # Sell signals
        df['sell'] = (df.price < df.ma)

        return df[['price', 'ma', 'buy', 'sell']]