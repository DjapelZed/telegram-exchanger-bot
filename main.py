import telebot, re, settings, db, dbapi
from threading import Thread
from exchanger import Exchanger
from datetime import datetime


bot = telebot.TeleBot(settings.BOT_KEY)
thread = Thread(target=dbapi.loop, args=(db.Database(),))
thread.start()


@bot.message_handler(commands=["start", "help"])
def start_message(message):
    print(message)
    response_message = "Hi! This bot will help you to get some information about currency rates."
    response_message += f"\nExchange the currency - /exchange [amount] [currency code] to [second currency code]"
    response_message += f"\nActual currency rates - /list"
    response_message += f"\nCurrency history - /list [currency code]"
    bot.reply_to(message, response_message)

# /list lst
@bot.message_handler(commands=["list", "lst"])
def get_latest(message):
        parts = [x for x in message.text.split()]
        data = None
        response_message = ""

        my_db = db.Database()

        def format_date(date):
            return date.strftime("%m/%d/%Y, %H:%M:%S")

        if len(parts) > 1:
            code = parts[1].upper()
            data = my_db.get_currency_history(code)
            response_message = f"<i>{code}</i>:\n"
            for row in data:
                response_message += f"<b>{format_date(row[2])}</b>: {row[1]:.2f}\n"
        else:
            data = my_db.get_currency_history()
            for row in data:
                response_message += f"<b>{row[0]}</b>: {row[1]:.2f}\n"

        my_db.close()
        bot.send_message(message.from_user.id, response_message, parse_mode = "HTML")


@bot.message_handler(commands=["exchange"])
def get_exchanged_value(message):
    default_error = "Unknown command format"

    def response(response_message):
        bot.send_message(message.from_user.id, response_message, parse_mode="HTML")

    try:
        parts = [x for x in message.text.lower().split()[1:] if x != "to"]
        if len(parts) < 2:
            response(default_error)
            return
        value_raw = parts[0].replace(",", ".")
        value = 0
        code_from = ""
        code_to = ""

        if value_raw[0] == "$":
            code_from = "USD"
            code_to = parts[1].upper()
            value = float(value_raw[1:])
        elif len(parts) == 3:
            code_from = parts[1].upper()
            code_to = parts[2].upper()
            value = float(value_raw)
        else:
            response(default_err)
            return


        my_db = db.Database()
        rate_from = my_db.get_currency_rate(code_from)
        rate_to = my_db.get_currency_rate(code_to)
        my_db.close()

        if not rate_from:
            response(f"Unknown currency code '{code_from}'")
            return
        if not rate_to:
            response(f"Unknown currency code '{code_to}'")
            return
        exchanged_value = value * rate_to[0] / rate_from[0]
        response(f"<b>{exchanged_value:.2f}</b> ({code_to})")
    except Exception as error:
        print(error)
        response("Unknown error")


bot.polling(none_stop = True)
dbapi.stop()
