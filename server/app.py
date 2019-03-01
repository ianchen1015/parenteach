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
    #print("Request body: " + body, "Signature: " + signature)
    #print(type(body))
    #print(json.loads(body)['events'][0]['message']['task'])

    event = json.loads(body)['events'][0]
    #print(event)

    def applyforleave() :
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                text="請選擇請假的類別",
                title="要請什麼假呢？",
                actions=[
                    PostbackTemplateAction(
                        label='事假',
                        text='事假',
                        data='action=setleavetime&leavetype=casual'
                    ),
                    PostbackTemplateAction(
                        label='病假',
                        text='病假',
                        data='leavetype=sick'
                    ),
                    PostbackTemplateAction(
                        label='其他',
                        text='其他',
                        data='leavetype=other'
                    )
                ]
            )
        )
        line_bot_api.push_message(user_id, buttons_template_message)

    def setleavetime():
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                text="請選擇日期和時間",
                title="從什麼時候開始請假？",
                actions=[
                    {
                        "type": "datetimepicker",
                        "label": "選擇日期和時間",
                        "data": "action=setleavetime",
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
        
    if event['type'] == 'postback':
        query = {}
        for item in event['postback']['data'].split('&'):
            query[item.split('=')[0]] = item.split('=')[1]
        print(query)

        if 'action' in query:
            if query['action'] == 'applyforleave':
                applyforleave()
            if query['action'] == 'setleavetime':
                setleavetime()

    return 'OK'

@app.route("/absent", methods=['GET'])
def absent():

    buttons_template_message = TemplateSendMessage(
        alt_text='您的孩子尚未到校',
        template=ButtonsTemplate(
            text='⚠️ 尚未到校\n今日 (1/03) 您的孩子 陳小明 尚未抵達教室，請問他是否需要請假呢？',
            actions=[
                PostbackTemplateAction(
                    label='開始請假',
                    text='開始請假',
                    data='action=applyforleave'
                )
            ]
        )
    )

    line_bot_api.push_message(user_id, buttons_template_message)

