from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('crvE525why6WynrVvNDD4EnXvEfWsAK4W8tjYHL18APUAkuI1NC6IpQhgytUXZ+yJFGfdDn9Nbi1jCikXABF1bsTEdN+6tU4TgAFOi/814UeOgJPrWTAWnTwwnk6rz97d5nETI2lMrGpdtNnijDP9QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('8ce8beaa96240ba2beb9a47fdff092fb')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    content = "{}: {}".format(event.source.user_id, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
