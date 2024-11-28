from collections import deque
from modules.wallet import Wallet


class TradingBotModel:
    def __init__(self, initial_investment=2000, trade_interval=300, max_prices=10, callback=None):
        """
        A data model to track the state of the trading bot.
        """
        self._callback = callback
        self.wallet = Wallet(usd_balance=initial_investment)
        self.trade_interval = trade_interval
        # Price history
        self._btc_prices = deque(maxlen=max_prices)
        self._eth_prices = deque(maxlen=max_prices)

        # Trade history
        self._trade_history = []

        # Latest prices

    @property
    def trade_history(self):
        """Return combined trade history."""
        return sorted(self._trade_history, key=lambda trade: trade.date, reverse=True)

    def add_trade(self, trade):
        """Add a trade to history."""
        self._trade_history.append(trade)
        self._trigger_callback()

    @property
    def btc_balance(self):
        """Return the BTC position."""
        return self.wallet.get_balance("BTC")

    @property
    def eth_balance(self):
        """Return the ETH position."""
        return self.wallet.get_balance("ETH")

    @property
    def usd_balance(self):
        """Return the USD balance."""
        return self.wallet.get_balance("USD")

    @property
    def btc_price(self):
        """Latest BTC price."""
        return self._btc_prices[-1] if self._btc_prices else 0

    @property
    def eth_price(self):
        """Latest ETH price."""
        return self._eth_prices[-1] if self._eth_prices else 0

    @property
    def total_balance(self):
        """Calculate the total balance in USD."""
        btc_value = self.btc_balance * self.btc_price
        eth_value = self.eth_balance * self.eth_price
        usd_value = self.usd_balance
        return btc_value + eth_value + usd_value

    def get_prices(self, symbol):
        """Get the price history for a symbol."""
        if symbol == "BTC":
            return list(self._btc_prices)
        elif symbol == "ETH":
            return list(self._eth_prices)

    def add_btc_price(self, price):
        """Add a new BTC price to the price history."""
        self._btc_prices.append(price)
        self._trigger_callback()

    def add_eth_price(self, price):
        """Add a new ETH price to the price history."""
        self._eth_prices.append(price)
        self._trigger_callback()

    def get_last_trade_price(self, symbol, action):
        """
        Get the price of the last trade for the given symbol and action (BUY or SELL).
        :param symbol: The symbol of the asset (e.g., "BTC" or "ETH").
        :param action: The type of trade (e.g., "BUY" or "SELL").
        :return: The price of the last trade or None if no such trade exists.
        """
        for trade in reversed(self._trade_history):  # Iterate from most recent to oldest
            if trade.symbol == symbol and trade.action.upper() == action.upper():
                return trade.price
        return None

    def _trigger_callback(self):
        if self._callback:
            self._callback()