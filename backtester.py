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
        df = df.copy()

        # Initialize portfolio tracking
        df['position'] = 0.0  # Number of shares held
        df['cash'] = self.initial_balance  # Available cash
        df['total_value'] = self.initial_balance  # Portfolio value

        for i in range(1, len(df)):
            # Carry forward previous values
            df.loc[df.index[i], 'position'] = df.loc[df.index[i - 1], 'position']
            df.loc[df.index[i], 'cash'] = df.loc[df.index[i - 1], 'cash']

            # Buy signal
            if df.loc[df.index[i], 'buy']:
                shares_to_buy = df.loc[df.index[i], 'cash'] / df.loc[df.index[i], 'price']
                df.loc[df.index[i], 'position'] += shares_to_buy
                df.loc[df.index[i], 'cash'] = 0.0

            # Sell signal
            if df.loc[df.index[i], 'sell']:
                df.loc[df.index[i], 'cash'] += df.loc[df.index[i], 'position'] * df.loc[df.index[i], 'price']
                df.loc[df.index[i], 'position'] = 0.0

            # Update total portfolio value
            df.loc[df.index[i], 'total_value'] = (
                    df.loc[df.index[i], 'cash'] +
                    df.loc[df.index[i], 'position'] * df.loc[df.index[i], 'price']
            )

        return {
            'final_balance': df['total_value'].iloc[-1],
            'return_pct': (df['total_value'].iloc[-1] / self.initial_balance - 1) * 100
        }