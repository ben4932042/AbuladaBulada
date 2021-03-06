from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv, find_dotenv
from dependencies import MySQL
from dependencies import Line
import configparser
import random
import re
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
    timestamp = int(event.timestamp)

    profile_dict = vars(profile)
    profile_id = profile_dict.get("user_id")    

    if msg.startswith("#insert"):
        try:
            msg_list = msg.split(" ")
            question = msg_list[1]
            answer = msg_list[2]

            sql_command=f"""INSERT INTO personal_talking (user_id, question, answer, timestamp)
                            VALUES ('{profile_id}', '{question}', '{answer}', {timestamp});"""

            MySQL(res_type="create").upload(sql_command=sql_command)

        except Exception as e:
            print(e)
            pretty_text = "failed"
        else:
            pretty_text = "success"
    elif msg.startswith("#get"):
        try:
            msg_query = msg.split(" ")[1]
            sql_command = f"SELECT answer FROM response_staging.personal_talking where question='{msg_query}'"
            data_return = MySQL(res_type="create").download(sql_command)

        except Exception as e:
            print(e)
            pretty_text = "failed"
        else:
            pretty_text = str(data_return[-1][0])
    elif msg == "法律查詢":
        pretty_text = "等待更新"

    else:
        pretty_text = Line(msg).judge_msg()


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=pretty_text)
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1234)
