import os
import datetime
from typing import List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Strategy Configuration
CONFIG = {
    'ma_window': 150,
    'buy_threshold': (0.005, 0.05),  # 0.5% to 5% above MA
    'initial_balance': 10_000,
    'tickers': ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META'],
    'data_dir': 'stocks',
    'test_years': 1
}

class DataManager:
    """Handles data downloading and loading operations"""

    @staticmethod
    def ensure_directory(path: str) -> None:
        """Create directory if it doesn't exist"""
        os.makedirs(path, exist_ok=True)

    @classmethod
    def download_data(cls, tickers: List[str], years: int = 1) -> None:
        """Download historical stock data from Yahoo Finance"""
        cls.ensure_directory(CONFIG['data_dir'])
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=years * 365)

        for ticker in tickers:
            try:
                df = yf.download(ticker, start=start_date, end=end_date)
                df = df[['Close']].rename(columns={'Close': 'price'})
                df['ma'] = df.price.rolling(CONFIG['ma_window']).mean()

                # Properly format and clean data before saving
                df = df.reset_index()
                df = df[['Date', 'price', 'ma']]  # Ensure correct column order
                df.to_csv(f"{CONFIG['data_dir']}/{ticker}.csv", index=False)
                print(f"Downloaded {ticker} ({len(df)} records)")
            except Exception as e:
                print(f"Error downloading {ticker}: {str(e)}")

    @staticmethod
    def load_data(ticker: str) -> Optional[pd.DataFrame]:
        """Load processed data from CSV with validation"""
        try:
            path = f"{CONFIG['data_dir']}/{ticker}.csv"
            df = pd.read_csv(path, parse_dates=['Date'], index_col='Date')

            # Force numeric conversion and clean data
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['ma'] = pd.to_numeric(df['ma'], errors='coerce')

            df = df.dropna().sort_index()
            return df[['price', 'ma']]
        except FileNotFoundError:
            print(f"Data file for {ticker} not found")
            return None


class TradingStrategy:
    """Implements 150MA trading logic"""

    @staticmethod
    def calculate_signals(df: pd.DataFrame) -> pd.DataFrame:
        """Generate buy/sell signals based on strategy rules"""
        df = df.copy()
        price, ma = df.price, df.ma

        # Calculate percentage difference from MA
        pct_diff = (price - ma) / ma

        # Buy conditions
        df['buy_signal'] = (
                (price > ma) &
                (pct_diff >= CONFIG['buy_threshold'][0]) &
                (pct_diff <= CONFIG['buy_threshold'][1])
        )

        # Sell conditions
        df['sell_signal'] = (price < ma)

        return df


class Backtester:
    """Handles strategy backtesting and performance analysis"""

    def __init__(self):
        self.portfolio = CONFIG['initial_balance']
        self.position = 0

    def run(self, df: pd.DataFrame) -> float:
        """Execute backtest using vectorized operations"""
        # Pre-calculate position changes
        df['position'] = 0
        df.loc[df.buy_signal, 'position'] = self.portfolio / df.price
        df.loc[df.sell_signal, 'position'] = 0

        # Forward fill positions between trades
        df['position'] = df.position.replace(0, method='ffill')

        # Calculate portfolio value
        df['value'] = df.position * df.price
        return df.value.iloc[-1]


def visualize_results(df: pd.DataFrame, ticker: str) -> None:
    """Generate professional visualization of trading signals"""
    plt.figure(figsize=(14, 7))

    plt.plot(df.price, label='Price', lw=1.5)
    plt.plot(df.ma, label=f'{CONFIG["ma_window"]}MA', ls='--', alpha=0.7)

    plt.scatter(df.index[df.buy_signal], df.price[df.buy_signal],
                marker='^', c='g', s=100, label='Buy Signal')
    plt.scatter(df.index[df.sell_signal], df.price[df.sell_signal],
                marker='v', c='r', s=100, label='Sell Signal')

    plt.title(f'{ticker} Trading Signals - 150MA Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(alpha=0.4)
    plt.tight_layout()
    plt.show()


def main():
    """Main execution flow"""
    # Data preparation
    DataManager.download_data(CONFIG['tickers'], CONFIG['test_years'])

    # Process each ticker
    for ticker in CONFIG['tickers']:
        if (df := DataManager.load_data(ticker)) is not None:
            # Strategy execution
            df = TradingStrategy.calculate_signals(df)
            final_value = Backtester().run(df)

            # Results reporting
            print(f"\n{ticker} Strategy Results:")
            print(f"Initial Balance: ${CONFIG['initial_balance']:,.2f}")
            print(f"Final Balance: ${final_value:,.2f}")
            print(f"Return: {(final_value / CONFIG['initial_balance'] - 1) * 100:.1f}%")

            visualize_results(df, ticker)


if __name__ == '__main__':
    main()