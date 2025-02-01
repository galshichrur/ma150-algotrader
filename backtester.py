"""
Backtesting engine for strategy validation
"""

import pandas as pd
from config import STRATEGY_CONFIG

class PortfolioManager:
    """Manages portfolio calculations and backtesting"""

    def __init__(self):
        self.initial_balance = STRATEGY_CONFIG['initial_balance']

    def run_backtest(self, df: pd.DataFrame) -> dict:
        """Execute vectorized backtest"""
        df['position'] = 0
        df.loc[df.buy, 'position'] = self.initial_balance / df.price
        df.loc[df.sell, 'position'] = 0
        df['position'] = df.position.ffill()
        df['value'] = df.position * df.price

        return {
            'final_balance': df.value.iloc[-1],
            'return_pct': (df.value.iloc[-1]/self.initial_balance - 1) * 100
        }