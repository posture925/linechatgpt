import requests

# 用來接收請求的 URL
line_bot_api = "https://api.line.me/v2/bot/message/reply"

# LINE Bot 的 Channel Access Token
header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_CHANNEL_ACCESS_TOKEN"
}

# 接收到的用戶訊息
received_text = "Hello, World!"

# 對用戶訊息進行回復
reply_text = "Hi, there!"

# 回復訊息的請求
post_data = {
    "replyToken": "REPLY_TOKEN",
    "messages": [
        {
            "type": "text",
            "text": reply_text
        }
    ]
}

# 發送回復請求
requests.post(line_bot_api, headers=header, json=post_data)