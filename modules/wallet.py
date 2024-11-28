

class Wallet:
    def __init__(self, usd_balance=0):
        self.balances = {"USD": usd_balance, "BTC": 0, "ETH": 0}

    def get_balance(self, symbol):
        return self.balances.get(symbol, 0)

    def has_sufficient_balance(self, symbol, amount, action, price):
        if action == "BUY":
            return self.balances["USD"] >= amount * price
        elif action == "SELL":
            return self.balances[symbol] >= amount
        return False

    def update_balance(self, symbol, amount, action, price):
        if action == "BUY":
            if self.balances["USD"] >= amount * price:
                self.balances["USD"] -= amount * price
                self.balances[symbol] += amount
            else:
                raise ValueError(f"Insufficient USD balance for BUY {symbol}.")
        elif action == "SELL":
            if self.balances[symbol] >= amount:
                self.balances["USD"] += amount * price
                self.balances[symbol] -= amount
            else:
                raise ValueError(f"Insufficient {symbol} balance for SELL.")


