from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('HkeS5olzirpiEOFlc2k4dhCdcKPr3SdAyWuTulioRuh2XHnCzNUA9nUPCCaYRjLoPwIDRCcYHv9cq/iAXcNQL0p/da4dgQn4WdJ27kx0+dYklBvYhGDVJ/3XC/n8vln3bW5/gzdoR9jQPZFQoO6lbwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f8c268a941dfc5049bf8b1dd76649b5')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get the request body as a dict
    body = request.get_json()
    print(body)

    # handle the event
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # send a request to the ChatGPT API
    response = requests.post(
        'https://api.openai.com/v1/models/chatgpt/generate',
        headers={
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json'
        },
        json={
            'prompt': event.message.text,
            'max_tokens': 128
        }
    )

    # get the response from the ChatGPT API
    chatgpt_response = response.json()

    # send the response back to the user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=chategpt_response['choices'][0]['text'])
    )

if __name__ == "__main__":
    app.run()