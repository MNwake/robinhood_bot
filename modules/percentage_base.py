from config.logging_config import logger
from modules.trading_utils import TradingStrategy

class PercentageBasedStrategy(TradingStrategy):
    def __init__(self, profit_margin, loss_margin, model, record_trade_callback):
        self.profit_margin = profit_margin
        self.loss_margin = loss_margin
        self.model = model
        self.record_trade = record_trade_callback

    def evaluate(self, symbol, current_price):
        wallet = self.model.wallet

        if current_price <= 0:
            logger.warning(f"Skipping evaluation for {symbol} due to invalid price: {current_price}")
            return

        # Get the last buy and sell prices from the price history
        prices = self.model.get_prices(symbol)
        last_buy_price = prices[-1] if prices else None
        last_sell_price = prices[-2] if len(prices) > 1 else None  # Example: second to last as a mock sell price

        # SELL Condition
        if last_buy_price:
            sell_threshold = last_buy_price * (1 + self.profit_margin)
            if current_price >= sell_threshold and wallet.get_balance(symbol) > 0:
                amount_to_sell = wallet.get_balance(symbol) * 0.5  # Sell 50%
                wallet.update_balance(symbol, amount_to_sell, "SELL", current_price)
                self.record_trade("Percentage Based", "SELL", symbol, amount_to_sell, current_price,
                                  wallet.get_balance("USD"), wallet.get_balance(symbol))

        # BUY Condition
        if last_sell_price:
            buy_threshold = last_sell_price * (1 - self.loss_margin)
            if current_price <= buy_threshold and wallet.get_balance("USD") > 0:
                amount_to_buy = (wallet.get_balance("USD") * 0.5) / current_price
                wallet.update_balance(symbol, amount_to_buy, "BUY", current_price)
                self.record_trade("Percentage Based", "BUY", symbol, amount_to_buy, current_price,
                                  wallet.get_balance("USD"), wallet.get_balance(symbol))
