import time
import logging
from abc import ABC, abstractmethod
from typing import Any
import requests

from logging_config import logger


# Trade execution logic with slippage simulation
def execute_trade(price, quantity, order_type, slippage=0.002):
    """
    Simulate trade execution with slippage.
    """
    if order_type == "BUY":
        adjusted_price = price * (1 + slippage)  # Increase price for buy trades
    elif order_type == "SELL":
        adjusted_price = price * (1 - slippage)  # Decrease price for sell trades
    else:
        raise ValueError(f"Invalid order type: {order_type}")

    logger.debug(
        f"Executing {order_type} trade: Original Price=${price:.2f}, Adjusted Price=${adjusted_price:.2f}, Quantity={quantity:.6f}, Slippage={slippage}"
    )
    return adjusted_price


# Dynamic position sizing
def calculate_position_size(cash_balance, price, risk_per_trade=0.02, atr=0.05):
    """
    Calculate position size based on risk per trade and volatility.
    """
    if price <= 0 or atr <= 0:
        logger.error(f"Invalid price ({price}) or ATR ({atr}) for position sizing.")
        raise ValueError(f"Invalid price ({price}) or ATR ({atr}) for position sizing.")

    risk_amount = cash_balance * risk_per_trade
    position_size = risk_amount / (atr * price)
    logger.debug(
        f"Calculated position size: Cash Balance=${cash_balance:.2f}, Price=${price:.2f}, ATR={atr:.2f}, Risk Amount=${risk_amount:.2f}, Position Size={position_size:.6f}"
    )
    return position_size


# Fetch crypto holdings
def check_crypto_holdings(api_client):
    """Fetch and return crypto holdings as a dictionary."""
    logger.info("Fetching crypto holdings...")
    try:
        holdings = api_client.get_holdings()
        if holdings and "results" in holdings:
            balances = {
                holding['asset_code']: float(holding['total_quantity'])
                for holding in holdings["results"]
            }
            logger.debug(f"Fetched holdings: {balances}")
            return balances
        else:
            logger.warning("No crypto holdings found or failed to fetch holdings.")
            return {}
    except Exception as e:
        logger.error(f"Error fetching crypto holdings: {e}", exc_info=True)
        return {}


# Fetch account balance
def fetch_account_balance(api_client):
    """Fetch and return account cash balance."""
    logger.info("Fetching account balance...")
    try:
        account_info = api_client.get_account()
        if account_info:
            cash_balance = float(account_info.get('buying_power', 0))
            currency = account_info.get('buying_power_currency', 'USD')
            logger.debug(f"Account Balance: {cash_balance:.2f} {currency}")
            return cash_balance, currency
        else:
            logger.warning("Failed to fetch account details. Check your credentials or API setup.")
            return 0, "USD"
    except Exception as e:
        logger.error(f"Error fetching account balance: {e}", exc_info=True)
        return 0, "USD"


# Fetch best bid and ask prices
def get_best_bid_ask(api_client, symbol: str):
    """Fetch and return best bid and ask prices for a trading pair."""
    logger.info(f"Fetching best bid and ask for {symbol}...")
    try:
        # Fetch data from API
        price_data = api_client.get_best_bid_ask(symbol)

        # Check if the response contains valid data
        if not price_data or "results" not in price_data:
            logger.warning(f"No valid results found for {symbol}. Response: {price_data}")
            return 0, 0

        # Extract the first result
        result = price_data["results"][0] if price_data["results"] else {}

        # Validate bid and ask values
        best_bid = float(result.get('bid_inclusive_of_sell_spread', 0))
        best_ask = float(result.get('ask_inclusive_of_buy_spread', 0))

        if best_bid > 0 and best_ask > 0:
            logger.debug(f"Best Bid: {best_bid:.2f}, Best Ask: {best_ask:.2f} for {symbol}")
            return best_bid, best_ask
        else:
            logger.warning(f"Invalid prices for {symbol}: Bid={best_bid}, Ask={best_ask}")
            return 0, 0
    except KeyError as e:
        logger.error(f"KeyError encountered for {symbol}: {e}. Response: {price_data}", exc_info=True)
    except ValueError as e:
        logger.error(f"ValueError converting bid/ask to float for {symbol}: {e}. Response: {price_data}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error fetching best bid and ask for {symbol}: {e}", exc_info=True)
    return 0, 0


# Fetch trading pairs
def fetch_trading_pairs(api_client):
    """Fetch and print trading pairs available on Robinhood."""
    logger.info("Fetching trading pairs...")
    try:
        pairs = api_client.get_trading_pairs()
        if pairs and "results" in pairs:
            for pair in pairs["results"]:
                symbol = pair.get("symbol", "Unknown")
                id = pair.get("id", "Unknown")
                logger.debug(f"Trading Pair - ID: {id}, Symbol: {symbol}")
            return pairs
        else:
            logger.warning("No trading pairs found or invalid response.")
            return None
    except Exception as e:
        logger.error(f"An error occurred while fetching trading pairs: {e}", exc_info=True)
        return None

class TradingStrategy(ABC):
    """
    Abstract base class for trading strategies.
    """
    @abstractmethod
    def evaluate(self, **kwargs):
        """
        Evaluate trading opportunities based on the strategy.
        """
        pass