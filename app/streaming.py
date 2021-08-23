# importing the required Libraries
import logging
import time
from kiteconnect import KiteTicker
import pyrebase
import json
import datetime
from token_store import token_key

from pymongo import MongoClient;
import bs4
import requests
import pandas as pd

client = MongoClient('50.116.32.224', 27017)
db = client["somy"]
dt_db = db["kiteconnect"]

# from .token_store import token_key
# from .consumers import tokens

# we store the firebase credentials here
# config = {
#     "apiKey": "AIzaSyCU9JP2yixeKjw3NE30Pb0I0D0UQjV94gA",
#     "authDomain": "kiteconnect-stock.firebaseapp.com",
#     "databaseURL": "https://kiteconnect-stock-default-rtdb.firebaseio.com",
#     "projectId": "kiteconnect-stock",
#     "storageBucket": "kiteconnect-stock.appspot.com",
#     "messagingSenderId": "981866107803",
#     "appId": "1:981866107803:web:568ffc6b464656a6f4c73e",
#     "measurementId": "G-9BRWTZYS5C"
# }
# Intialising the firebase with the specified credentials

# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()

logging.basicConfig(level=logging.DEBUG)
# api_key = open('/home/akkey/Desktop/Django-projects/django-sockets/demo1/integers/api_key.txt', 'r').read()
# Geting the API access token 
api_key = "0yvny102khsjlnpr"
# access_token = str(database.child("access_token").get().val())
access_token = "935u0J7CisocVaO13jmETQ1eetnvWrXi"
print("HIIIiiiiii")
print(access_token)
# "P0XqJpx45l6wZJNSx0lXrqEK1b61QXZl"
# tokens = [5215745, 633601, 1195009, 779521, 758529, 1256193, 194561, 1837825, 952577, 1723649, 3930881, 4451329, 593665, 3431425, 2905857, 3771393, 3789569, 3463169, 381697, 54273, 415745, 2933761, 3580417, 49409, 3060993, 4464129, 3375873, 4574465, 636673, 3721473, 2796801]
tokens = token_key

new_dict = {}
for t in tokens:
    new_dict[str(t)] = {}
# @sync_to_async
closed = True


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def to_dic(ticks):
    for data in ticks:
        last_price = data['last_price']
        close = data['ohlc']['close']
        change = data['change']
        ins_tok = data['instrument_token']
        new_dict[str(ins_tok)] = {'instrument_token': ins_tok, 'close': close, 'change': change,
                                  'last_price': last_price}

    return new_dict


kws = KiteTicker(api_key, access_token)


def on_ticks(ws, ticks):
    print('check:',ticks)
    try:
        year = datetime.datetime.now().year
        now = datetime.datetime.now()
        today_day = now.strftime("%A")
        weekend_day = ('Saturday', 'Sunday')
        if today_day in weekend_day:
            print('market closed due to weekend')
        else:
            print('market open no weekend today')
            BASE_URL = "https://zerodha.com/z-connect/traders-zone/holidays/"
            ROUTE = "trading-holidays-{}-nse-bse-mcx"

            url = BASE_URL + ROUTE.format(year)

            r = requests.get(url)
            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.text, 'lxml')

                tables = soup.findAll("table")
                df = None
                for table in tables:
                    df = pd.read_html(str(table))[0]
                    break

                if df is not None and not df.empty:
                    # print("Holidays ... ")
                    # print(df)
                    holidays = df.to_dict("records")

                    new = 0
                    holiday_dt = set()
                    for holiday in holidays:
                        name = holiday.get("Holidays")
                        date = datetime.datetime.strptime(holiday.get("Date"), "%B %d, %Y")
                        holiday_dt.add(str(date.date()))

                    to_dt = pd.to_datetime('today').date()
                    if str(to_dt) in holiday_dt:
                        print('market is closed holiday')
                        pass
                    else:
                        print('market is open')
                        dic = to_dic(ticks)
                        x = dt_db.find()
                        val = x.count(True)

                        if val < 1:
                            dt_db.insert_one({"a": 0, "Stock": dic})
                        else:
                            dt_db.update_many({"a": 0},
                                              {
                                                  "$set": {

                                                      "Stock": dic
                                                  },
                                                  "$currentDate": {"lastModified": True}

                                              })


    except Exception as e:
        print('error in ticks : ', e)
        pass


def on_connect(ws, response):
    # update_token()
    print("hellooooooo")
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL, tokens)


def on_close(ws, code, reason):
    # access_token = str(database.child("access_token").get().val())
    # kws = KiteTicker(api_key, access_token)
    # kws.on_ticks = on_ticks
    # kws.on_connect = on_connect
    # kws.on_close = on_close
    # kws.connect()
    print("Stream stopped! Reconnecting")


kws.on_ticks = on_ticks
kws.on_connect = on_connect
# kws.on_close = on_close
# kws.on_reconnect = on_reconnect

print('Hiiiiiiiiiiiiiiiiii')
# kws.connect()
kws.connect(threaded=True)
print('HIIIIIIIIIIIIII')

while True:
        print("Recheck")
        # new_access_token = str(database.child("access_token").get().val())
        new_access_token = "935u0J7CisocVaO13jmETQ1eetnvWrXi"
        if access_token != new_access_token:
            access_token = new_access_token
            print("NEW")
            kws = KiteTicker(api_key, access_token)
            kws.on_ticks = on_ticks
            kws.on_connect = on_connect
            kws.on_close = on_close
            kws.connect(threaded= True)
        time.sleep(3)
