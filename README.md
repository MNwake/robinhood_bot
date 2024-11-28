# Trading Bot Simulator

A Python-based **Trading Bot Simulator** designed to test and optimize various trading strategies using real-time market data. This project is a part of my software development portfolio and is currently **in development**. The primary goal of this application is to simulate trading strategies and analyze their performance over time, making it an excellent tool for backtesting and learning about algorithmic trading.

---

## 🚀 Features

### **Current Features**
- **Real-Time Data Integration**: Fetch live price data for Bitcoin (BTC) and Ethereum (ETH) from Robinhood's API.
- **Simulated Trades**: Execute simulated BUY and SELL trades based on customizable strategies.
- **Moving Average Strategy**: Implements a moving average-based trading strategy.
- **Wallet Management**: Tracks balances in USD, BTC, and ETH with real-time valuation in USD.
- **Trade History**: Logs all trades with details, including price, amount, strategy used, and balances.
- **Live UI Updates**: Kivy-based graphical interface for real-time monitoring of balances, prices, and trade history.

---

## 🛠️ Planned Features

### **Simulation Enhancements**
- **Cash Management**: Add inputs for deposits and withdrawals to simulate real-life trading scenarios.
- **Advanced Trade Insights**: Provide more detailed analysis for each trade, such as profit/loss metrics, trade duration, and strategy-specific performance.

### **Deployment-Ready Features**
- **Robinhood Integration**: Expand from simulation to execute real trades using the Robinhood API.
- **Risk Management Tools**: Implement stop-loss and take-profit settings to control trade risks.
- **Strategy Performance Dashboard**: Add visual insights for long-term strategy analysis, including ROI and trade win/loss ratios.
- **Multi-Asset Support**: Extend support to additional cryptocurrencies or stocks.

---

## ⚡ Getting Started

### **Prerequisites**
To test this application, you need the following:
- **Python 3.8 or later**
- **Environment Variables**:
  - `ROBINHOOD_API_KEY`: Your Robinhood API key
  - `ROBINHOOD_PRIVATE_KEY`: Your private key for Robinhood authentication

---

## 📈 Usage

### **How It Works**
1. The bot fetches real-time price data for BTC and ETH.
2. Trades are simulated based on the configured trading strategy (e.g., moving average crossover).
3. Balances and trade history are updated in real-time.
4. Insights into trade performance are logged for analysis.

### **Current Limitations**
- The bot **does not execute real trades** (yet).
- Still under development—use with caution.

---

## 🤝 Contributing
Contributions are welcome! If you have ideas for improving the simulator or additional features you'd like to see, feel free to open an issue or create a pull request.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📝 Note
This project is for **simulation purposes only**. It is not a financial product, and I am not responsible for any losses incurred if this code is adapted for real trading.
