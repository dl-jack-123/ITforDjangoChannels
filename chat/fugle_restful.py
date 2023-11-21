#chat/fugle.py
import time

from fugle_marketdata import WebSocketClient, RestClient
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
import channels.layers
import django, sys
from os.path import join, dirname, abspath
from os import environ
from datetime import datetime


# ---------------------- django setting --------------------------
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

#  Set the correct path to you settings module
environ.setdefault("DJANGO_SETTINGS_MODULE", "django_channels.settings")

# All django stuff has to come after the setup:
django.setup()

# ---------------------- django setting --------------------------
channel_layer = channels.layers.get_channel_layer()

YOUR_API_KEY = 'xxx'

async def main():
    from fugle_marketdata import RestClient

    client = RestClient(api_key=YOUR_API_KEY)
    stock = client.stock
    _dt = None
    while True:

        data = stock.snapshot.movers(market='TSE', direction='up', change='percent')


        await channel_layer.group_send("chat_ranking", {'type': 'ranking.message', "message": data})
        time.sleep(10)



if __name__ == '__main__':
    asyncio.run(main())


