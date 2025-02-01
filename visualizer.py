"""
Visualization module for strategy results
"""

import matplotlib.pyplot as plt
import pandas as pd
from config import STRATEGY_CONFIG

class StrategyVisualizer:
    """Generates professional visualizations of trading activity"""

    def __init__(self):
        self.style = 'seaborn-v0_8'  # Updated style name
        self.ma_window = STRATEGY_CONFIG['ma_window']

    def plot_signals(self, df: pd.DataFrame, ticker: str):
        """Plot price, MA, and trading signals"""
        plt.style.use(self.style)

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(df.price, label='Price', lw=1)
        ax.plot(df.ma, label=f'{self.ma_window}MA', ls='--', alpha=0.7)

        ax.scatter(df.index[df.buy], df.price[df.buy],
                   marker='^', c='g', s=100, label='Buy')
        ax.scatter(df.index[df.sell], df.price[df.sell],
                   marker='v', c='r', s=100, label='Sell')

        ax.set_title(f'{ticker} - 150MA Trading Signals')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()