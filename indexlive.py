from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
#from api.chatgpt import ChatGPT
import chatgpt

import os
#line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
#line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))



line_handler = WebhookHandler('2f8c268a941dfc5049bf8b1dd76649b5')
line_bot_api = LineBotApi('HkeS5olzirpiEOFlc2k4dhCdcKPr3SdAyWuTulioRuh2XHnCzNUA9nUPCCaYRjLoPwIDRCcYHv9cq/iAXcNQL0p/da4dgQn4WdJ27kx0+dYklBvYhGDVJ/3XC/n8vln3bW5/gzdoR9jQPZFQoO6lbwdB04t89/1O/w1cDnyilFU=')


working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
app = Flask(__name__)
chatgpt = chatgpt()

# domain root
@app.route('/')
def home():
    return 'Hello, World!'
@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        return
    working_status = True
    if working_status:
        chatgpt.add_msg(f"Human:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))
if __name__ == "__main__":
    app.run()