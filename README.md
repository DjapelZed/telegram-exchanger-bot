# telegram-exchanger-bot
This bot for Telegram parse and sends some information about currency rates.

# How to use

1. Clone this repo
1. Get the access key from [exchangeratesapi.io](exchangeratesapi.io)
1. Get the Telegram bot token from [Telegram API](https://core.telegram.org/bots#6-botfather)
1. Create PostgreSQL database:
   ```sql
   CREATE TABLE currency_history
    (
    id        serial                              NOT NULL
        CONSTRAINT currency_history_pk
            PRIMARY KEY,
    code      varchar(10)                         NOT NULL,
    value     double precision                    NOT NULL,
    timestamp timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

    ALTER TABLE currency_history
      OWNER TO developer;

    CREATE UNIQUE INDEX currency_history_id_uindex
      ON currency_history (id);
    ```
1. Edit `settings.py` by inserting your tokens and database info
1. `pip install -r requirements.txt`
1. Run `main.py`
