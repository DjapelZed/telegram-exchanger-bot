from exchanger import Exchanger
from threading import Thread
from time import sleep


is_work = True


def stop():
    global is_work
    is_work = False


def loop(db):
    global is_work
    exchanger = Exchanger()
    while is_work:
        rates = exchanger.get_latest()
        db.insert_rates(rates)
        db.commit()
        print("inserted")
        sleep(60*10)
    db.close()
