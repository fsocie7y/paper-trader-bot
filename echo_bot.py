import os
import requests
import random

from bs4 import BeautifulSoup
from telebot import TeleBot

TIMEFRAMES = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]
URL = "https://paper-trader.frwd.one/"
BOT_KEY = os.environ.get("BOT_KEY")

bot = TeleBot(BOT_KEY, parse_mode=None)


def get_image(pair: str) -> str | bool:
    params = {
        "pair": pair,
        "timeframe": random.choice(TIMEFRAMES),
        "candles": random.randint(1, 1000),
        "ma": random.randint(1, 100),
        "tp": random.randint(1, 100),
        "sl": random.randint(1, 100),
    }

    response = requests.post(URL, data=params)

    img_parse = BeautifulSoup(response.text, 'html.parser').findAll('img')
    if img_parse:
        img_url = f"{URL}{img_parse[0]['src']}"
        return img_url
    return False


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello it's your Paper Trader bot.\nPlease enter your pair in next format.\n"
        "Example pair: BTCUSDT"
        "Enter /help to see help.\n"
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "You can use only existing pairs in upper or lower case\n"
        "Please enter pairs by example: BTCUSDT or btcusdt"
    )


@bot.message_handler(content_types=["text"])
def send_pair_img(message):
    img = get_image(message.text)
    if img:
        bot.send_photo(message.chat.id, img)
    else:
        bot.send_message(message.chat.id, "Please enter correct data or /help to see rules.")


bot.infinity_polling()
