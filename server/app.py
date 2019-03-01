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

# leaving apply parameters
leave_start_time = ''
leave_end_time = ''
leave_type = ''
leave_reason = ''
setting_leave_reason = False

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    global setting_leave_reason, leave_start_time, leave_end_time, leave_type, leave_reason

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
                title="下次來學習是哪時候呢？",
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
                        text='事假',
                        data='action=setleavereason&leavetype=casual&datatype=leavetype'
                    ),
                    PostbackTemplateAction(
                        label='病假',
                        text='病假',
                        data='action=setleavereason&leavetype=sick&datatype=leavetype'
                    ),
                    PostbackTemplateAction(
                        label='其他',
                        text='其他',
                        data='action=setleavereason&leavetype=other&datatype=leavetype'
                    )
                ]
            )
        )
        line_bot_api.push_message(user_id, buttons_template_message)

    def setleavereason():
        global setting_leave_reason
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
        setting_leave_reason = True

    def endofapplyleave():

        message = TextSendMessage(
            text="了解，感謝告知！\n{}\n{}\n{}\n{}".format(leave_start_time, leave_end_time, leave_type, leave_reason)
        )

        line_bot_api.push_message(user_id, message)

    def cancelleave():

        setting_leave_reason = False

        message = TextSendMessage(
            text="取消請假"
        )

        line_bot_api.push_message(user_id, message)

    event = json.loads(body)['events'][0]

    if setting_leave_reason == True:
        leave_reason = event['message']['text']
        setting_leave_reason = False
        endofapplyleave()
    else:
        if event['type'] == 'postback':
            query = {}
            for item in event['postback']['data'].split('&'):
                query[item.split('=')[0]] = item.split('=')[1]
            print(query)

            if 'action' in query:
                if query['action'] == 'setleavestarttime':
                    setleavestarttime()
                if query['action'] == 'setleaveendtime':
                    setleaveendtime()
                if query['action'] == 'setleavetype':
                    setleavetype()
                if query['action'] == 'setleavereason':
                    setleavereason()
                    return 'ok'
                if query['action'] == 'endofapplyleave':
                    endofapplyleave()
                if query['action'] == 'cancelleave':
                    cancelleave()
            if 'datatype' in query:
                if query['datatype'] == 'startdate':
                    leave_start_time = event['postback']['params']['datetime']
                if query['datatype'] == 'enddate':
                    leave_end_time = event['postback']['params']['datetime']
                if query['datatype'] == 'leavetype':
                    leave_type = query['leavetype']

    print('###', leave_start_time, leave_end_time, leave_type, leave_reason, setting_leave_reason)

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
                    data='action=setleavestarttime'
                )
            ]
        )
    )

    line_bot_api.push_message(user_id, buttons_template_message)

@app.route("/a", methods=['GET'])
def q():
    message = TextSendMessage(
        text='qwe'
    )

    line_bot_api.push_message(user_id, message)