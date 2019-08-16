import json
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
    return "<p>Hello World!" + "<br>" + "Taiwan : " + str(d1)\
           + "<br>"+"Japan : " + str(d2)\
           + "<br>"+"Los_Angeles : " + str(d3) + "</p>"


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
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text: str = event.message.text
    user_id = event.source.user_id
    if text == "time" or text == "時間":
        d1 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Taipei"))
        d2 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Tokyo"))
        d3 = datetime.datetime.now().astimezone(pytz.timezone("America/Los_Angeles"))
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text="Taiwan : " + str(d1)\
                                                        + "\n"+"Japan : " + str(d2)\
                                                        + "\n"+"Los_Angeles : "+ str(d3)))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_id + " say : " + text))


if __name__ == '__main__':
    app.run()
