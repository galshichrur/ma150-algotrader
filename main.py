"""
Main execution module for 150MA trading strategy
"""

from data_manager import DataHandler
from strategy import TradingStrategy
from backtester import PortfolioManager
from visualizer import StrategyVisualizer

def main():
    # Initialize components
    data_handler = DataHandler()
    strategy = TradingStrategy()
    backtester = PortfolioManager()
    visualizer = StrategyVisualizer()

    # Data pipeline
    data_handler.download_market_data()

    # Process each ticker
    for ticker in data_handler.config['tickers']:
        print(f"\nAnalyzing {ticker}...")

        # Load and process data
        df = data_handler.load_ticker_data(ticker)
        if df is None:
            continue

        # Generate signals
        df = strategy.generate_signals(df)

        # Backtest strategy
        results = backtester.run_backtest(df)

        # Display results
        print(f"\n📈 {ticker} Results:")
        print(f"Initial Balance: ${backtester.initial_balance:,.2f}")
        print(f"Final Balance: ${results['final_balance']:,.2f}")
        print(f"Return: {results['return_pct']:.1f}%")

        # Visualize
        visualizer.plot_signals(df, ticker)

if __name__ == '__main__':
    main()