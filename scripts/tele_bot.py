#! /usr/bin/python2
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, \
    ReplyKeyboardMarkup, KeyboardButton

import requests
import sys
import os


# Add django as interface to Databse
import django
django.setup()
from django_cat_app.models import UserLog


# if run locally, we can read the TOKEN from a file, as fallback (if e.g. run on heroku, we use an
# environment variable)
try:
    from secret_chat_key import TELEGRAM_TOKEN
except ImportError as e:  # Exception as e:
    try:
        TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    except KeyError:
        print("'TELEGRAM_TOKEN' not in ENV")
    print("Read TELEGRAM_TOKEN from env")


def get_random_cat_url():
    response = requests.get(url="https://api.thecatapi.com/v1/images/search")
    cat_url = str(response.json()[0]['url'])
    return cat_url


class DemoTelegramBot:
    def __init__(self):

        # activate webhooks (instead of polling)
        self.with_webhooks = False
        try:
            self.with_webhooks = os.environ['WITH_HOOK']
        except KeyError:
            pass

        self.updater = Updater(token=TELEGRAM_TOKEN)

        if self.with_webhooks:
            port = int(os.environ.get('PORT', '8443'))  # is set by Heroku if run there
            print("Running with webhook on port %i" % port)
            self.updater.start_webhook(listen="0.0.0.0", port=port, url_path=TELEGRAM_TOKEN)
            self.updater.bot.set_webhook("https://telegramcatbott.herokuapp.com/" + TELEGRAM_TOKEN)

        self.dispatcher = self.updater.dispatcher

        # create callbacks for some commands
        self.dispatcher.add_handler(CommandHandler("help", self.on_help))
        self.dispatcher.add_handler(CommandHandler("options", self.on_options))
        self.dispatcher.add_handler(CommandHandler("location", self.on_location))
        self.dispatcher.add_handler(CommandHandler("cat", self.on_cat))


        # Callback for normal messages from user
        # This function also contains the Database-counter(!)
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text_cb))

        # Callback for position
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.got_location, edited_updates=True))

        # callback for custom keyboards
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.mode_button_cb))

    @staticmethod
    def on_options(bot, update):
        # encode question in callback_data ('w'): hack, could be something better
        keyboard = [[InlineKeyboardButton("Bad", callback_data='w,1'),
                     InlineKeyboardButton("OK", callback_data='w,2'),
                     InlineKeyboardButton("Great", callback_data='w,3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('How is the weather today?', reply_markup=reply_markup)

    @staticmethod
    def mode_button_cb(bot, update):
        assert isinstance(update, Update)
        assert isinstance(update.callback_query, CallbackQuery)
        # user_id = update.callback_query.from_user.id

        query = update.callback_query

        ans = query.data.split(',')
        cmd = str(ans[0])
        value = int(ans[1])

        if cmd == 'w':
            text = "Weather score of %i" % value
        else:
            text = "Unhandled callback_data %s" % query.data
            print(text)

        # Replace keyboard with this message to clean up the window
        bot.edit_message_text(text=text, chat_id=query.message.chat_id, message_id=query.message.message_id)

    @staticmethod
    def text_cb(bot, update):
        assert isinstance(update, Update)

        # used to identify users. Is not unique, but we don't want to store unique personal information by design
        first_name = update.message.chat.first_name

        ul, created = UserLog.objects.get_or_create(user_id=first_name)
        assert isinstance(ul, UserLog)
        ul.cat_count += 1
        ul.save()

        # print (update) -> https://www.cleancss.com/python-beautify/
        print("Got text: %s, cat_count: %i" % (str(update.message.text), ul.cat_count))
        msg = "Hello %s: %s (you can also use /help) (this is your cat nr %i)" % (first_name,
                                                                                  update.message.text.upper(),
                                                                                  ul.cat_count)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        bot.send_photo(chat_id=update.message.chat_id, photo=get_random_cat_url())

    @staticmethod
    def got_location(bot, update):
        assert isinstance(update, Update)

        if update.edited_message:
            message = update.edited_message
        else:
            message = update.message

        a, b = message.location.latitude, message.location.longitude
        bot.send_message(chat_id=message.chat_id, text="You are at %.3f, %.3f" % (a, b))

    @staticmethod
    def on_location(bot, update):
        location_keyboard = [[KeyboardButton(text="Send my location", request_location=True)]]
        update.message.reply_text('Please share your location.',
                                  reply_markup=ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True))

    @staticmethod
    def on_help(bot, update):
        update.message.reply_text(u'Send any message to get an uppercase response. \n'
                                  u'/location to send your location \n️'
                                  u'/cat to get a cat image \n️'
                                  u'/options to talk about weather️ ☺')

    @staticmethod
    def on_cat(bot, update):
        bot.send_photo(chat_id=update.message.chat_id, photo=get_random_cat_url())

    def run(self):
        if not self.with_webhooks:
            print("Start polling")
            sys.stdout.flush()
            self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    dtb = DemoTelegramBot()
    dtb.run()
