import os
import inspect

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from utils import (
    get_steam_game_image_url, is_number, generate_caption, get_game_prices
)


class SteamShopHelper:

    def __init__(self):
        self.updater = Updater(
            token=os.environ.get("teletoken")[:-1],
            use_context=True
        )
        self.non_command_methods = ["run", "get_command_methods"]

    @staticmethod
    def hi(update: Update, context: CallbackContext):
        update.message.reply_text("Hi")

    @staticmethod
    def send_photo(update: Update, context: CallbackContext):
        user_input = update.message.text.split()[1:]
        if not all(is_number(inp) for inp in user_input):
            update.message.reply_text("لطفا فقط APP ID گیم را وارد کنید.")
            return
        for appid in user_input:
            prices = get_game_prices(appid)
            caption = generate_caption(prices)
            update.message.reply_photo(
                photo=get_steam_game_image_url(appid),
                caption=caption+"\n\n"+"خرید: "+"@"+update.effective_user.username
            )

    def run(self):
        dispatcher = self.updater.dispatcher
        cmd_methods = self._get_command_methods()
        for method_name, method in cmd_methods:
            dispatcher.add_handler(
                CommandHandler(method_name, method)
            )

        self.updater.start_polling()

    def _get_command_methods(self):
        all_methods = inspect.getmembers(SteamShopHelper, predicate=inspect.isfunction)
        return [
            func for func in all_methods
            if not func[0].startswith("__")
            and func[0] not in self.non_command_methods
        ]


bot = SteamShopHelper()
bot.run()
