import logging

from collections import deque

from logging_config import logger
from modules.trading_utils import TradingStrategy, calculate_position_size

class MovingAverageStrategy(TradingStrategy):
    def __init__(self, short_window, long_window, model, record_trade_callback, required_profit_percent=1.0):
        self.moving_averages = {
            "BTC": MovingAverage(short_window, long_window),
            "ETH": MovingAverage(short_window, long_window),
        }
        self.model = model
        self.record_trade = record_trade_callback
        self.required_profit_percent = required_profit_percent / 100  # Convert percentage to decimal

    def evaluate(self, symbol, price):
        ma = self.moving_averages[symbol]  # Get the specific MovingAverage instance
        short_ma, long_ma = ma.update(price)

        if not short_ma or not long_ma:
            return

        if price <= 0:
            logger.warning(f"Skipping evaluation for {symbol} due to invalid price: {price}")
            return

        # Fetch wallet information
        wallet = self.model.wallet

        # Get last trade prices
        last_buy_price = self.model.get_last_trade_price(symbol, "BUY")
        last_sell_price = self.model.get_last_trade_price(symbol, "SELL")

        # BUY Condition
        if short_ma > long_ma and wallet.get_balance("USD") > 100:  # Ensure a minimum USD balance
            # Check if the current price is below the last buy price by the required margin
            if last_buy_price is None or price < last_buy_price * (1 - self.required_profit_percent):
                amount_to_buy = (wallet.get_balance("USD") * 0.5) / price
                if amount_to_buy > 0:  # Prevent zero/negative trades
                    wallet.update_balance(symbol, amount_to_buy, "BUY", price)
                    self.record_trade("Moving Average", "BUY", symbol, amount_to_buy, price,
                                      wallet.get_balance("USD"), wallet.get_balance(symbol))
                else:
                    logger.warning(f"Skipping BUY for {symbol} due to insufficient calculated amount to buy.")

        # SELL Condition
        elif short_ma < long_ma and wallet.get_balance(symbol) > 0:
            # Check if the current price is above the last sell price by the required margin
            if last_sell_price is None or price > last_sell_price * (1 + self.required_profit_percent):
                amount_to_sell = (wallet.get_balance(symbol) * 0.5)  # Sell 50% of holdings
                if amount_to_sell > 0:  # Prevent zero/negative trades
                    wallet.update_balance(symbol, amount_to_sell, "SELL", price)
                    self.record_trade("Moving Average", "SELL", symbol, amount_to_sell, price,
                                      wallet.get_balance("USD"), wallet.get_balance(symbol))
                else:
                    logger.warning(f"Skipping SELL for {symbol} due to insufficient calculated amount to sell.")


class MovingAverage:
    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window
        self.short_sum = 0
        self.long_sum = 0
        self.short_ma = deque(maxlen=short_window)
        self.long_ma = deque(maxlen=long_window)

    def update(self, price):
        logger.debug(f"Updating moving averages with new price: {price}")

        if len(self.short_ma) == self.short_window:
            logger.debug(f"Removing oldest short_window value: {self.short_ma[0]}")
            self.short_sum -= self.short_ma[0]
        if len(self.long_ma) == self.long_window:
            logger.debug(f"Removing oldest long_window value: {self.long_ma[0]}")
            self.long_sum -= self.long_ma[0]

        self.short_ma.append(price)
        self.long_ma.append(price)
        self.short_sum += price
        self.long_sum += price

        short_ma = self.short_sum / self.short_window if len(self.short_ma) == self.short_window else None
        long_ma = self.long_sum / self.long_window if len(self.long_ma) == self.long_window else None

        logger.debug(f"Short MA: {short_ma}, Long MA: {long_ma}")
        return short_ma, long_ma
