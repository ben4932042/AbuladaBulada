from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv, find_dotenv
from dependencies import MySQL
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
    profile = line_bot_api.get_profile(event.source.user_id)
    msg = event.message.text
    msg_list = msg.split("_")
    print(msg)
    profile_dict = vars(profile)
    ID = profile_dict.get("user_id")    

    if msg_list[0] == "test":
        try:
            question = msg_list[1]
            answer = msg_list[2]
            MySQL(res_type="create")\
                    .upload(sql_command=f"""INSERT INTO personal_talking (user_id, question, answer)
                                         VALUES ('{ID}', '{question}', '{answer}');""")
        except Exception as e:
            print(e)
            pretty_text = "failed"
        else:
            pretty_text = "success"
    else:
        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=pretty_text)
    )

if __name__ == "__main__":
    app.run()
