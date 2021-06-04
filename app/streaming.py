import logging
import time
from kiteconnect import KiteTicker
import pyrebase
import json
import datetime
from token_store import token_key
#from .token_store import token_key
# from .consumers import tokens


config = {
    "apiKey": "AIzaSyCU9JP2yixeKjw3NE30Pb0I0D0UQjV94gA",
    "authDomain": "kiteconnect-stock.firebaseapp.com",
    "databaseURL": "https://kiteconnect-stock-default-rtdb.firebaseio.com",
    "projectId": "kiteconnect-stock",
    "storageBucket": "kiteconnect-stock.appspot.com",
    "messagingSenderId": "981866107803",
    "appId": "1:981866107803:web:568ffc6b464656a6f4c73e",
    "measurementId": "G-9BRWTZYS5C"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

logging.basicConfig(level=logging.DEBUG)
# api_key = open('/home/akkey/Desktop/Django-projects/django-sockets/demo1/integers/api_key.txt', 'r').read()
api_key = "0yvny102khsjlnpr"
access_token = str(database.child("access_token").get().val())
print("HIIIiiiiii")
print(access_token)
#"P0XqJpx45l6wZJNSx0lXrqEK1b61QXZl"
# tokens = [5215745, 633601, 1195009, 779521, 758529, 1256193, 194561, 1837825, 952577, 1723649, 3930881, 4451329, 593665, 3431425, 2905857, 3771393, 3789569, 3463169, 381697, 54273, 415745, 2933761, 3580417, 49409, 3060993, 4464129, 3375873, 4574465, 636673, 3721473, 2796801]
tokens = token_key

new_dict = {}
for t in tokens:
    new_dict[t] = {}
# @sync_to_async
def myconverter(o):
    if isinstance(o, datetime.datetime):
             return o.__str__()

def to_dic(ticks):
    
    for data in ticks:
        last_price = data['last_price']
        close = data['ohlc']['close']
        change = data['change']
        ins_tok = data['instrument_token']
        new_dict[ins_tok] = {'close': close, 'change': change, 'last_price': last_price}
    print(len(new_dict))
    return new_dict


kws = KiteTicker(api_key, access_token)
def on_ticks(ws, ticks):
    print("Hiiemowe")
    access_token = str(database.child("access_token").get().val())
    dic = to_dic(ticks)
    print(len(ticks))
    database.update({"Stock": dic})
   

def on_connect(ws, response):
    # update_token()
    print("hellooooooo")
    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_FULL, tokens)

def on_close(ws, code, reason):
    print("Stream stopped! Reconnecting")

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

print ('Hiiiiiiiiiiiiiiiiii')
kws.connect()
print ('HIIIIIIIIIIIIII')
