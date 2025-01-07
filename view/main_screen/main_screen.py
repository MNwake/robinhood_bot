from kivy.properties import StringProperty, ListProperty
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText

from view.base_screen import BaseScreenView


class MainScreenView(BaseScreenView):
    usd_balance = StringProperty("0.00")
    btc_balance = StringProperty("0.0000")
    eth_balance = StringProperty("0.0000")
    total_balance = StringProperty("0.00")
    btc_price = StringProperty("$0.00")
    eth_price = StringProperty("$0.00")
    trade_history = ListProperty([])

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
        # Retrieve balances from Wallet
        self.usd_balance = f"${self.model.bot.usd_balance:.2f}"
        self.btc_balance = f"{self.model.bot.btc_balance:.4f}"
        self.eth_balance = f"{self.model.bot.eth_balance:.4f}"
        self.total_balance = f'${self.model.bot.total_balance:.2f}'
        # Retrieve prices from the model
        self.btc_price = f"${self.model.bot.btc_price:.2f}" if self.model.bot.btc_price else "$0.00"
        self.eth_price = f"${self.model.bot.eth_price:.2f}" if self.model.bot.eth_price else "$0.00"


        # Retrieve trade history
        self.trade_history = self.model.bot.trade_history  # Pass full trade history to property

        # Update the trade history list in the view
        self.populate_trade_history()
        self.update_start_stop_icon()

    def populate_trade_history(self):
        """Populate the trade history list in the UI."""
        self.ids.trade_history_list.clear_widgets()

        for trade in self.trade_history:
            # Create and format the list item content
            headline = f"{trade.formatted_date()} - {trade.action} {trade.amount:.4f} {trade.symbol}"
            supporting_text = f"Strategy: {trade.strategy}, Price: ${trade.price:.2f}"
            tertiary_text = (
                f"Balances - USD: ${trade.usd_balance:.2f}, {trade.symbol}: {trade.symbol_balance:.4f}"
            )

            # Add a new MDListItem with three lines
            self.ids.trade_history_list.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text=headline,
                    ),
                    MDListItemSupportingText(
                        text=supporting_text,
                    ),
                    MDListItemTertiaryText(
                        text=tertiary_text,
                    ),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint_x=0.9,
                )
            )

    def start_stop_button(self):
        """Toggle the bot state and update the icon."""
        if not self.model.is_bot_running:
            self.controller.start_bot()
        else:
            self.controller.stop_bot()

    def update_start_stop_icon(self):
        """Update the start/stop button icon based on bot state."""
        start_stop_button = self.ids.start_stop_button
        start_stop_button.icon = "play-circle-outline" if not self.model.is_bot_running else "stop-circle-outline"
