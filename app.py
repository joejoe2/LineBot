import json
import requests
import sys
import datetime
import pytz
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi(
    'uJ6LnR2TWpOmYqSYW9yg1nSe1GO9+c3euzndfcjTeTSlfz1r58dfBxpnNySHjq7/oUAmiO0VBDHb5HyLSdnu+PXMA71HJkbT4jwqfTDXhpXRAWOFsEVbpjbDNahvbXVLVh9cZsTLH+yB3cxwMsyC/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('905c2e3f57145acb7d791c46dec9a573')

app = Flask(__name__)


@app.route('/')
def index():
    d1 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Taipei"))
    d2 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Tokyo"))
    d3 = datetime.datetime.now().astimezone(pytz.timezone("America/Los_Angeles"))
    return "<p>Hello World!" + "<br>" + get_time(sep="<br>") + "</p>"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        print("received post at /callback")
        sys.stdout.flush()
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret")
        sys.stdout.flush()
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text: str = event.message.text
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    if text.lower().startswith("[time]") or text.startswith("[時間]"):
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=get_time("\n")))
    elif text.startswith("[with luis score]"):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=get_luis(text.replace("[with luis score]",""))))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_name + " say : " + text))


def get_time(sep="\n"):
    d1 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Taipei"))
    d2 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Tokyo"))
    d3 = datetime.datetime.now().astimezone(pytz.timezone("America/Los_Angeles"))
    return "Taiwan : "+str(d1)+sep+"Japan : "+str(d2)+sep+"Los_Angeles : "+str(d3)


def get_luis(text):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '83ca8ec7e88c4e7bbf45c063080b3b68',
    }

    params = {
        # Query parameter
        'q': text,
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
    }

    try:
        r = requests.get(
            "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/d85bc3b4-80a6-4c0d-8aae-79627ca915d4",
            headers=headers, params=params)
        return r.json()

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
