#chat/fugle_websocket.py
import time

from fugle_marketdata import WebSocketClient
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
import channels.layers
import django, sys
from os.path import join, dirname, abspath
from os import environ
import json

# ---------------------- django setting --------------------------
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

#  Set the correct path to you settings module
environ.setdefault("DJANGO_SETTINGS_MODULE", "django_channels.settings")

# All django stuff has to come after the setup:
django.setup()

# ---------------------- django setting --------------------------
channel_layer = channels.layers.get_channel_layer()

YOUR_API_KEY = 'YTRiNWNhZjYtNGRjNS00MDIyLTlhZTQtY2E1MTI0NzU0NjI4IDQyODc2ZTMxLThlNWEtNDMyMy1iMTYyLTIzN2MyYTBkNGVkNg'

def handle_message(message):
    print(message)
    message = json.loads(message)
    if message['event'] in ['data']:
        data = message['data']
        symbol = data['symbol']

        async_to_sync(channel_layer.group_send)(f"chat_{symbol}",
                                                {'type': 'trades.message', "message": message})


async def main():
    client = WebSocketClient(api_key=YOUR_API_KEY)
    stock = client.stock
    stock.on('message', handle_message)
    await stock.connect()
    stock.subscribe({
        'channel': 'trades',
        'symbol': '2330'
    })

if __name__ == '__main__':
    asyncio.run(main())

