from kivy.clock import Clock

from model.base_model import BaseScreenModel
from modules.trading_bot_model import TradingBotModel


class MainScreenModel(BaseScreenModel):
    """
    Implements the logic of the MainScreenView class.
    """

    def __init__(self):
        super().__init__()

        self.bot = TradingBotModel(initial_investment=2000, trade_interval=300, callback=self.callback)
        self._is_bot_running = False  # Private attribute to track the bot's state

    @property
    def is_bot_running(self):
        """
        Property to get the current state of the bot.
        """
        return self._is_bot_running

    @is_bot_running.setter
    def is_bot_running(self, value):
        """
        Setter to update the bot's running state. Triggers the callback on change.
        """
        if self._is_bot_running != value:
            self._is_bot_running = value
            self.callback()  # Notify observers when the state changes

    def callback(self):
        """
        Notify observers safely on the main thread.
        """
        Clock.schedule_once(lambda dt: self.notify_observers('main screen'))