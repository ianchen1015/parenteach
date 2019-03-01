from flask import Flask, request, abort
import json

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

user_id = 'Ue171fd928b7c3dee72656c700742be92'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    print(type(body))
    print(json.loads(body)['events'][0]['message']['task'])

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

    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)

    line_bot_api.push_message(user_id, TextSendMessage(text=profile.display_name+profile.user_id+profile.picture_url+profile.status_message))

    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackAction(
                    label='postback',
                    text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text'
                ),
                URIAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )
    line_bot_api.push_message(user_id, buttons_template_message)

@app.route("/absent", methods=['GET'])
def absent():

    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            text='⚠️ 尚未到校\n今日 (1/03) 您的孩子 陳小明 尚未抵達教室，請問他是否需要請假呢？',
            actions=[
                PostbackTemplateAction(
                    label='開始請假',
                    #text='postback text',
                    data='applyforleave'
                )
            ]
        )
    )

    line_bot_api.push_message(user_id, buttons_template_message)

@app.route("/applyforleave", methods=['GET'])
def applyForLeave():

    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            text="請選擇日期和時間",
            title="從什麼時候開始請假？",
            actions=[
                {
                    "type": "datetimepicker",
                    "label": "選擇日期和時間",
                    "data": "資料 1",
                    "mode": "datetime",
                    "initial": "2019-01-12T07:00",
                    "max": "2020-01-12T07:00",
                    "min": "2018-01-12T07:00"
                },
                {
                    "type": "message",
                    "label": "不請假了",
                    "text": "取消請假"
                }
            ]
        )
    )

    line_bot_api.push_message(user_id, buttons_template_message)



