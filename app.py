from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv, find_dotenv
import configparser

import random
load_dotenv(find_dotenv())
app = Flask(__name__)


line_bot_api = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
            
    pretty_note = '♫♪♬'
    pretty_text = ''
        
    for i in event.message.text:
        
        pretty_text += i
        pretty_text += random.choice(pretty_note)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=pretty_text)
    )

if __name__ == "__main__":
    app.run()
