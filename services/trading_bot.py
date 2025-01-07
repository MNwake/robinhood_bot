import time
from datetime import datetime
from threading import Thread

import pytz
from config.logging_config import logger
from modules.moving_average import MovingAverageStrategy
from modules.percentage_base import PercentageBasedStrategy
from modules.trade_history import TradeHistoryModel
from modules.trading_utils import get_best_bid_ask
from robinhood_api_trading import CryptoAPITrading


class TradingBot:
    def __init__(self, model):
        """
        Initialize the trading bot with a model and strategies.
        """
        self.is_running = False
        self.thread = None
        self.model = model  # Instance of TradingBotModel

        # Initialize strategies directly
        # Initialize strategies directly
        self.strategies = [
            PercentageBasedStrategy(0.05, 0.05, model, self.record_trade),
            MovingAverageStrategy(5, 20, model, self.record_trade, required_profit_percent=10),
        ]

        # API Client
        self.api_client = CryptoAPITrading()
        usd_balance = model.wallet.get_balance("USD")
        logger.info("TradingBot initialized with initial investment of $%.2f.", usd_balance)

    def start(self):
        """
        Start the bot in a separate thread.
        """
        if not self.is_running:
            self.is_running = True
            self.thread = Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        """
        Signal the bot to stop running.
        """
        self.is_running = False
        if self.thread:
            self.thread.join()

    def run(self):
        """
        Start the trading bot.
        """
        logger.info("Starting live trading simulation...")
        while self.is_running:
            try:
                # Fetch live prices for BTC and ETH
                btc_price = self.fetch_live_prices("BTC-USD")
                eth_price = self.fetch_live_prices("ETH-USD")

                # Append latest prices to sliding window
                self.model.add_btc_price(btc_price)
                self.model.add_eth_price(eth_price)

                logger.info(
                    f"Latest Prices - BTC: ${btc_price:.2f}, ETH: ${eth_price:.2f}, Time: {self.get_est_time()}"
                )

                # Run percentage-based strategy
                for strategy in self.strategies:
                    strategy.evaluate("BTC", btc_price)
                    strategy.evaluate("ETH", eth_price)

                # Sleep until the next interval
                time.sleep(self.model.trade_interval)

            except Exception as e:
                logger.error(f"Error occurred: {e}", exc_info=True)
                break

    def record_trade(self, strategy, action, symbol, amount, price, usd_balance, symbol_balance):
        trade = TradeHistoryModel(
            strategy=strategy,
            action=action,
            symbol=symbol,
            amount=amount,
            price=price,
            usd_balance=usd_balance,
            symbol_balance=symbol_balance,
        )
        self.model.add_trade(trade)

    def fetch_live_prices(self, symbol):
        """
        Fetch live prices (best bid and ask) for a specific symbol and return the mid-price.
        Retries up to 3 times if the API response is invalid, with a 5-minute wait between attempts.
        """
        retries = 3  # Number of retry attempts
        wait_time = 300  # Wait time in seconds (5 minutes)

        for attempt in range(retries):
            bid, ask = get_best_bid_ask(self.api_client, symbol)

            if bid > 0 and ask > 0:
                mid_price = (bid + ask) / 2
                logger.debug(f"Fetched Prices for {symbol} - Bid: ${bid:.2f}, Ask: ${ask:.2f}, Mid: ${mid_price:.2f}")
                return mid_price
            else:
                logger.warning(
                    f"Attempt {attempt + 1} failed to fetch valid prices for {symbol}. Retrying in {wait_time // 60} minutes...")
                time.sleep(wait_time)

        # If all retries fail, raise an exception or return 0 as the fallback behavior
        logger.error(f"Failed to fetch valid prices for {symbol} after {retries} attempts.")
        return 0

    @staticmethod
    def get_est_time():
        """Get the current time in EST."""
        utc_time = datetime.now(tz=pytz.utc)
        est_time = utc_time.astimezone(pytz.timezone("US/Eastern"))
        return est_time.strftime("%Y-%m-%d %H:%M:%S %Z")
