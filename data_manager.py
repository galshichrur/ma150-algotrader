"""
Handles data acquisition and management
"""

import os
import pandas as pd
import yfinance as yf
from config import STRATEGY_CONFIG

class DataHandler:
    """Manages data download and storage operations"""

    def __init__(self):
        self.config = STRATEGY_CONFIG
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Create data directory if missing"""
        os.makedirs(self.config['data_dir'], exist_ok=True)

    def download_market_data(self):
        """Download historical price data for all tickers"""
        for ticker in self.config['tickers']:
            self._download_ticker_data(ticker)

    def _download_ticker_data(self, ticker: str):
        """Download and process data for individual ticker"""
        try:
            df = yf.download(
                ticker,
                start=self.config['start_date'],
                end=self.config['end_date']
            )
            self._process_and_save(df, ticker)
            print(f"✅ Successfully downloaded {ticker}")
        except Exception as e:
            print(f"❌ Failed to download {ticker}: {str(e)}")

    def _process_and_save(self, df: pd.DataFrame, ticker: str):
        """Process raw data and save to CSV"""
        df = df[['Close']].rename(columns={'Close': 'price'})
        df['ma'] = df.price.rolling(self.config['ma_window']).mean()
        df.reset_index(inplace=True)
        df.to_csv(f"{self.config['data_dir']}/{ticker}.csv", index=False)

    def load_ticker_data(self, ticker: str) -> pd.DataFrame:
        """Load processed data for analysis"""
        path = f"{self.config['data_dir']}/{ticker}.csv"
        if not os.path.exists(path):
            return None

        df = pd.read_csv(path, parse_dates=['Date'], index_col='Date')
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        return df[['price', 'ma']]