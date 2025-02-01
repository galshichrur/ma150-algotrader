"""
Configuration settings for 150MA trading strategy
"""

from datetime import datetime, timedelta

STRATEGY_CONFIG = {
    'ma_window': 150,
    'buy_threshold': (0.005, 0.05),  # 0.5% to 5% above MA
    'initial_balance': 10_000,
    'tickers': ['SPY', 'QQQ', 'PLTR', 'TSLA', 'NVDA', 'DDOG', 'AFRM', 'ANET', 'BMY', 'CRM'],
    'data_dir': 'data', 
    'start_date': datetime.today() - timedelta(days=365*5),
    'end_date': datetime.today()
}