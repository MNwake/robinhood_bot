from view.main_screen.main_screen import MainScreenView
from services.trading_bot import TradingBot


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    """

    def __init__(self, model):
        self.model = model  # MainScreenModel
        self.view = MainScreenView(controller=self, model=self.model)
        self.bot = TradingBot(model=self.model.bot)  # Pass the TradingBotModel to the bot logic

    def get_view(self) -> MainScreenView:
        return self.view

    def start_bot(self):
        """
        Start the trading bot.
        """
        if not self.bot.is_running:
            self.bot.start()  # Calls TradingBot.run() in a thread

            self.model.is_bot_running = True

    def stop_bot(self):
        """
        Stop the trading bot.
        """
        if self.bot.is_running:
            self.bot.stop()  # Calls a method in TradingBot to stop the bot gracefully
            self.model.is_bot_running = False
