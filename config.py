"""
Configuration settings for 150MA trading strategy
"""

from datetime import datetime, timedelta

STRATEGY_CONFIG = {
    'ma_window': 150,
    'buy_threshold': (0.005, 0.05),  # 0.5% to 5% above MA
    'initial_balance': 10_000,
    'tickers': ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'META'],
    'data_dir': 'data',
    'test_years': 1,
    'start_date': datetime.today() - timedelta(days=365),
    'end_date': datetime.today()
}