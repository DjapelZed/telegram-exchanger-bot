# telegram-exchanger-bot
This bot for Telegram parse and sends some information about currency rates.

# How to use

1. Clone this repo
1. Get the access key from [exchangeratesapi.io](exchangeratesapi.io)
1. Get the Telegram bot token from [Telegram API](https://core.telegram.org/bots#6-botfather)
1. Create PostgreSQL database and `CURRENCY_HISTORY` table with 
   * `ID` integer 
   * `CODE` varchar(10)
   * `VALUE` double precision
   * `TIMESTAMP` timestamp  
1. Edit `settings.py` by inserting your tokens and database info
1. `pip install -r requirements.txt`
1. Run `main.py`
