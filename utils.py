import csv
import os

import requests


def save_to_csv(data, filename):
    """Save historical price data to a CSV file."""
    if os.path.exists(filename):
        os.remove(filename)  # Remove the existing file
        print(f"Deleted existing file: {filename}")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "price"])  # Header row
        writer.writerows(data)
    print(f"Saved new data to {filename}")


def load_from_csv(filename):
    """
    Load historical price data from a CSV file.
    Adjusts the file path to ensure compatibility with the directory structure.
    """
    # Get the current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Resolve the file path relative to the script directory
    filepath = os.path.join(script_dir, filename)

    # Check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist.")

    # Load the CSV file
    with open(filepath, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return [[int(row[0]), float(row[1])] for row in reader]


def get_historical_prices_coingecko_append(symbol: str, vs_currency: str = "usd", days: int = 1, filename: str = "prices.csv"):
    """
    Fetch historical price data from CoinGecko and append to a CSV file if it already exists.
    :param symbol: Cryptocurrency symbol, e.g., 'bitcoin'.
    :param vs_currency: Currency to fetch prices against, e.g., 'usd'.
    :param days: Number of days of historical data.
    :param filename: CSV filename to save/load data.
    :return: List of [timestamp, price] pairs.
    """
    new_data = []

    print(f"Fetching historical prices for {symbol}...")
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        new_data = response.json()["prices"]  # Returns a list of [timestamp, price]
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return []

    if os.path.exists(filename):
        # Load existing data and merge
        print(f"Appending to existing file: {filename}")
        existing_data = load_from_csv(filename)
        combined_data = existing_data + [row for row in new_data if row not in existing_data]  # Prevent duplicates
        save_to_csv(combined_data, filename)
        return combined_data
    else:
        # Save as new file if it doesn't exist
        print(f"Creating new file: {filename}")
        save_to_csv(new_data, filename)
        return new_data


btc_prices = get_historical_prices_coingecko_append("bitcoin", days=1, filename="btc_prices.csv")
eth_prices = get_historical_prices_coingecko_append("ethereum", days=1, filename="eth_prices.csv")
