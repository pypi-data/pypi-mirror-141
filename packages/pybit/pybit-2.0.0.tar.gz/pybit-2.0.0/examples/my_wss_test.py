from pybit import inverse_perpetual, usdt_perpetual, spot
from time import sleep

import logging
logging.basicConfig(filename="websocket_restructure_wss_example.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


api_key = ""
api_secret = ""
test = True  # testnet or mainnet


def callback(message):
    print(f"callback()")
    print(message)
    pass


# Inverse and USDT perpetual subscription:
inverse_ws = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws1 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws2 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws3 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws4 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws5 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws6 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws7 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws8 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws9 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws10 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws11 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws12 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws13 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws14 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws15 = inverse_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
inverse_ws.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws1.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws2.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws3.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws4.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws5.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws6.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws7.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws8.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws9.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws10.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws11.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws12.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws13.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws14.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])
inverse_ws15.instrument_info_stream(callback, ["BTCUSD", "ETHUSD"])


'''
usdt_ws = usdt_perpetual.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
usdt_instrument_info_sub = usdt_ws.custom_topic_stream(usdt_perpetual.PUBLIC_WSS, "instrument_info.100ms.BTCUSDT", callback)
usdt_position_sub = usdt_ws.custom_topic_stream(usdt_perpetual.PRIVATE_WSS, "position", callback)


# Spot subscription:
spot_ws = spot.WebSocket(test=test, api_key=api_key, api_secret=api_secret)
spot_v1_trade_sub = spot_ws.trade_v1_stream(callback)
spot_outbound_account_info_sub = spot_ws.outbound_account_info_stream(callback)'''
'''Spot custom subscription:
spot_v1_trade_sub = spot_ws.custom_topic_stream(
    {"topic": "trade","event": "sub","symbol": "BTCUSDT","params": {"binary":False}},
    callback,
    spot.PUBLIC_V1_WSS
)
spot_outbound_account_info_sub = spot_ws.custom_topic_stream(
    "outboundAccountInfo", callback, spot.PRIVATE_WSS
)
'''


while True:
    # Proceed with trading strategy whilst still receiving callbacks for new
    #  websocket messages
    print(1)
    sleep(1)


