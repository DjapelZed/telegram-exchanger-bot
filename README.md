# telegram-exchanger-bot
This bot for Telegram parse and sends some information about currency rates.

# How to use

1. Clone this repo
2. Get the access key from exchangeratesapi.io
3. Create PostgreSQL database CURRENCY_HISTORY with 
  * ID (integer) 
  * CODE (varchar(10))
  * VALUE (double precision)
  * TIMESTAMP (timestamp)  
