import psycopg2, sys, datetime, settings
from psycopg2 import Error


class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user=settings.DB_USER,
                                          password=settings.DB_PASSWORD,
                                          host=settings.DB_HOST,
                                          database=settings.DB,
                                          port=settings.DB_PORT)
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            raise


    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Соединение с PostgreSQL закрыто")


    def get_currency_history(self, code = None):
        if code is None:
            self.cursor.execute("SELECT DISTINCT ON (CODE) CODE, VALUE, TIMESTAMP FROM CURRENCY_HISTORY ORDER BY CODE, TIMESTAMP DESC")
        else:
            params = (code,)
            self.cursor.execute("SELECT CODE, VALUE, TIMESTAMP FROM CURRENCY_HISTORY WHERE CODE = %s ORDER BY TIMESTAMP DESC", params)
        items = self.cursor.fetchall()
        return items


    def get_currency_rate(self, code):
        select_query = f"SELECT VALUE FROM CURRENCY_HISTORY WHERE CODE = %s ORDER BY TIMESTAMP DESC"
        params = (code,)
        self.cursor.execute(select_query, params)
        items = self.cursor.fetchone()
        return items


    def insert_rate(self, code, value):
        insert_query = "INSERT INTO CURRENCY_HISTORY (CODE, VALUE, TIMESTAMP) VALUES (%s, %s, %s)"
        params = (code, value, datetime.datetime.now())
        self.cursor.execute(insert_query, params)


    def insert_rates(self, rates):
        for rate in list(rates.keys()):
            self.insert_rate(rate, rates[rate])


    def commit(self):
        self.connection.commit()
