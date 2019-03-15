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

# simulate database
data = {}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    event = json.loads(body)['events'][0]

    user_id = event['source']['userId']

    if user_id not in data:
        data[user_id] = {
            'leave_start_time': '',
            'leave_end_time': '',
            'leave_type': '',
            'leave_reason': '',
            'setting_leave_reason': False # store next message if true
        }

    def setleavestarttime():
        buttons_template_message = TemplateSendMessage(
            alt_text='選擇請假時間',
            template=ButtonsTemplate(
                text="請選擇日期和時間",
                title="從什麼時候開始請假？",
                actions=[
                    {
                        "type": "datetimepicker",
                        "label": "選擇日期和時間",
                        "data": "action=setleaveendtime&datatype=startdate",
                        "mode": "datetime",
                        "initial": "2019-01-12T07:00",
                        "max": "2020-01-12T07:00",
                        "min": "2018-01-12T07:00",
                        "text": "時間已選擇"
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

    def setleaveendtime():
        buttons_template_message = TemplateSendMessage(
            alt_text='選擇請假時間',
            template=ButtonsTemplate(
                text="請選擇日期和時間",
                title="下次來學校是哪時候呢？",
                actions=[
                    {
                        "type": "datetimepicker",
                        "label": "選擇日期和時間",
                        "data": "action=setleavetype&datatype=enddate",
                        "mode": "datetime",
                        "initial": "2019-01-12T07:00",
                        "max": "2020-01-12T07:00",
                        "min": "2018-01-12T07:00",
                        "text": "時間已選擇"
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

    def setleavetype() :
        buttons_template_message = TemplateSendMessage(
            alt_text='請選擇請假的類別',
            template=ButtonsTemplate(
                text="請選擇請假的類別",
                title="要請什麼假呢？",
                actions=[
                    PostbackTemplateAction(
                        label='事假',
                        data='action=setleavereason&leavetype=casual&datatype=leavetype'
                    ),
                    PostbackTemplateAction(
                        label='病假',
                        data='action=setleavereason&leavetype=sick&datatype=leavetype'
                    ),
                    PostbackTemplateAction(
                        label='其他',
                        data='action=setleavereason&leavetype=other&datatype=leavetype'
                    )
                ]
            )
        )
        line_bot_api.push_message(user_id, buttons_template_message)

    def setleavereason():
        buttons_template_message = TemplateSendMessage(
            alt_text='請告知請假原因',
            template=ButtonsTemplate(
                text="方便的話，還想了解一下請假的原因喔！\n（請以一則訊息說明）",
                actions=[
                    PostbackTemplateAction(
                        label='不請假了',
                        text='取消請假',
                        data='action=cancelleave'
                    )
                ]
            )
        )

        line_bot_api.push_message(user_id, buttons_template_message)
        data[user_id]['setting_leave_reason'] = True

    def endofapplyleave():

        leave_reason_show = {
            'casual': '事假',
            'sick': '病假',
            'other': '其他'
        }

        message = TextSendMessage(
            text="了解，感謝告知！\n\n{}\n{}\n{}\n{}".format(
                '從 ' + data[user_id]['leave_start_time'].replace('T', ' '),
                '到 ' + data[user_id]['leave_end_time'].replace('T', ' '),
                '類別：' + leave_reason_show[data[user_id]['leave_type']],
                '原因：' + data[user_id]['leave_reason'])
        )

        line_bot_api.push_message(user_id, message)

    def cancelleave():

        data[user_id]['setting_leave_reason'] = False

        message = TextSendMessage(
            text="取消請假"
        )

        line_bot_api.push_message(user_id, message)

    # response message
    if event['type'] == 'message':
        # response keywords
        if event['message']['text'] == '我要請假':
            setleavestarttime()

        # store message
        if data[user_id]['setting_leave_reason'] == True:
            # store leave reason
            data[user_id]['leave_reason'] = event['message']['text']
            data[user_id]['setting_leave_reason'] = False
            endofapplyleave()

    # postback response
    if event['type'] == 'postback':
        query = {}
        for item in event['postback']['data'].split('&'):
            query[item.split('=')[0]] = item.split('=')[1]

        if 'action' in query:
            # call function by function name string
            function_name = query['action']
            locals()[function_name]()
        if 'datatype' in query:
            # store data
            if query['datatype'] == 'startdate':
                data[user_id]['leave_start_time'] = event['postback']['params']['datetime']
            if query['datatype'] == 'enddate':
                data[user_id]['leave_end_time'] = event['postback']['params']['datetime']
            if query['datatype'] == 'leavetype':
                data[user_id]['leave_type'] = query['leavetype']

    return 'OK'

@app.route("/absent", methods=['GET'])
def absent():

    buttons_template_message = TemplateSendMessage(
        alt_text='您的孩子尚未到校',
        template=ButtonsTemplate(
            text='⚠️ 尚未到校\n今日 (1/03) 您的孩子尚未抵達教室，請問他是否需要請假呢？',
            actions=[
                PostbackTemplateAction(
                    label='開始請假',
                    text='開始請假',
                    data='action=setleavestarttime'
                )
            ]
        )
    )
    user_id = 'Ue171fd928b7c3dee72656c700742be92'
    line_bot_api.push_message(user_id, buttons_template_message)
