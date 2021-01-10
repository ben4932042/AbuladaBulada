from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction



line_bot_api = LineBotApi("29cc5993-388e-430a-9a21-70b037327f19")
handler = WebhookHandler("0ce2b2b0d7c0c4e0c34e20bfe3a47c22")



app = Flask(__name__)

@app.route("/", methods=['POST'])
def callback():
    return "OK"

if __name__ == "__main__":

    app.run()

