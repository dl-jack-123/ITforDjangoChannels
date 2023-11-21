# chat/consumers.py
import json
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Product, Quote

from fugle_marketdata import RestClient

api_key = 'xxx'
#

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        client = RestClient(api_key=api_key)
        self.stock = client.stock

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        message = f"""
歡迎來到 {self.room_name} 股票排行推播聊天室
            """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['message'] == '查詢目前價格':
            obj = Quote.objects.filter(symbol=self.room_name).order_by('-datetime').first()
            message = f'查詢字串: {text_data_json["message"]}\n'
            message += f"{obj.datetime}, {self.room_name} {obj.name}, 現在價格: {obj.closePrice} 量: {obj.lastSize}\n"
            self.send(text_data=json.dumps({"message": message}))


    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def candles_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        msg = f'現在時間為: {message["date"]}, ' + f','.join([f' {i}: {j}' for i,j in message.items() if i != 'date'])
        self.send(text_data=json.dumps({"message": msg}))

    def trades_message(self, event):
        data = event["message"]

        # Send message to WebSocket
        dt = datetime.fromtimestamp(data['data']['time'] / 10**6)
        msg = f"{dt}, {self.room_name} 現在價格: {data['data']['price']} 總量: {data['data']['volume']}\n"
        self.send(text_data=json.dumps({"message": msg}))

    def ranking_message(self, event):
        data = event["message"]

        # Send message to WebSocket
        msg = f'--------------------------------------------------------更新時間{datetime.now()}\n'
        for ind, i in enumerate(data['data'][:10]):
            msg += f'No.{ind} {i["symbol"]}, {i["name"]}, 價格:{i["closePrice"]}, 漲跌:{i["change"]}, 漲跌幅:{i["changePercent"]}\n'
        msg += '--------------------------------------------------------'
        self.send(text_data=json.dumps({"message": msg}))




