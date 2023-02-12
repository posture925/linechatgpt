# ch36_4.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

handler = WebhookHandler('2f8c268a941dfc5049bf8b1dd76649b5')
line_bot_api = LineBotApi('HkeS5olzirpiEOFlc2k4dhCdcKPr3SdAyWuTulioRuh2XHnCzNUA9nUPCCaYRjLoPwIDRCcYHv9cq/iAXcNQL0p/da4dgQn4WdJ27kx0+dYklBvYhGDVJ/3XC/n8vln3bW5/gzdoR9jQPZFQoO6lbwdB04t89/1O/w1cDnyilFU=')

# 收 Line 訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# Echo 回應, 相當於學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo_message(event):
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()





