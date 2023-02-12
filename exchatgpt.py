import requests
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)

handler = WebhookHandler('2f8c268a941dfc5049bf8b1dd76649b5')


# LINE Bot API URL
line_bot_api = "https://api.line.me/v2/bot/message/reply"

# LINE Bot API 憑證
line_bot_token = "HkeS5olzirpiEOFlc2k4dhCdcKPr3SdAyWuTulioRuh2XHnCzNUA9nUPCCaYRjLoPwIDRCcYHv9cq/iAXcNQL0p/da4dgQn4WdJ27kx0+dYklBvYhGDVJ/3XC/n8vln3bW5/gzdoR9jQPZFQoO6lbwdB04t89/1O/w1cDnyilFU="

# OpenAI API URL
openai_api = "https://api.openai.com/v1/engines/davinci/jobs"

# OpenAI API 憑證
openai_token = "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"

# 回復用戶訊息
#@app.route("/callback", methods=['POST'])

def reply(event):
    # 取得用戶訊息

    user_message = event["message"]["text"]

    # 通過 OpenAI API 請求得到 ChatGPT 的回答
    openai_response = requests.post(
        openai_api,
        headers={
            "Authorization": "Bearer " + openai_token
        },
        json={
            "prompt": user_message,
            "max_tokens": 128,
            "temperature": 0.5
        }
    )

    # 取得 ChatGPT 的回答
    chatgpt_answer = openai_response.json()["choices"][0]["text"]

    # 回復給用戶
    requests.post(
        line_bot_api,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + line_bot_token
        },
        json={
            "replyToken": event["replyToken"],
            "messages": [
                {
                    "type": "text",
                    "text": chatgpt_answer
                }
            ]
        }
    )

# 接收訊息的 Webhook
'''
def webhook(request):
    # 取得請求的 JSON 資料
    request_json = request.get_json()

    # 回復每一個用戶的訊息
    for event in request_json["events"]:
        reply(event)

    # 回傳 200 OK
    return "OK"
'''

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
app.run()
