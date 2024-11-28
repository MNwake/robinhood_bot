from datetime import datetime


class TradeHistoryModel:
    def __init__(self, strategy, action, symbol, amount, price, usd_balance, symbol_balance, date=None):
        """
        A model to represent a single trade in the bot's history.
        """
        self.strategy = strategy
        self.action = action  # 'BUY' or 'SELL'
        self.symbol = symbol
        self.amount = amount
        self.price = price
        self.usd_balance = usd_balance
        self.symbol_balance = symbol_balance
        self.date = date if date else datetime.now()

    def formatted_date(self):
        """Return the date in the format MM-DD HH:MM."""
        return self.date.strftime("%m-%d %H:%M")

    def __repr__(self):
        return (
            f"Trade("
            f"Date: {self.date}, "
            f'Strategy: {self.strategy}'
            f"Action: {self.action}, "
            f"Symbol: {self.symbol}, "
            f"Amount: {self.amount:.4f}, "
            f"Price: ${self.price:.2f}, "
            f"USD Balance: ${self.usd_balance:.2f}, "
            f"{self.symbol} Balance: {self.symbol_balance:.4f}"
            f")"
        )