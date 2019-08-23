import json
from json import JSONDecodeError
import random
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

unknown_msg = ["我聽不懂", "請用更具體的命令", "我不明白，請說清楚一點"]
greet_msg = ["你好", "哈囉", "嗨~"]
greet_morning_msg = ["早安", "早", "早上好"]
greet_afternoon_msg = ["午安", "下午好"]
greet_night_msg = ["晚安"]
greet_bye_msg = ["再見", "掰掰", "下次見"]


@app.route('/')
def index():
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


@app.route("/broadcast", methods=['GET'],)
def broadcast():
    body = request.args.get("data")
    line_bot_api.broadcast(TextSendMessage(text="test broadcast push : "+str(body)))
    # print(body)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text: str = event.message.text
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    pic_url = profile.picture_url
    status = profile.status_message

    if text.lower().startswith("[time]") or text.startswith("[時間]"):
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=get_time("\n")))
    elif text.startswith("[with luis score]"):
        send_text = get_luis(text.replace("[with luis score]", ""))
        reply = ""
        try:
            obj = json.loads(send_text)
            # print(obj["topScoringIntent"]["intent"], obj["topScoringIntent"]["score"])
            reply = get_reply(obj["topScoringIntent"]["intent"], obj["topScoringIntent"]["score"])
        except JSONDecodeError as ex:
            print(ex.msg)

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=send_text+"\n"+reply))
    elif text.startswith("[my info]"):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="id : " + user_id + "\n" + "name : " + user_name))
    elif text.startswith("[followers]"):
        t = text[text.find("{")+1:text.find("}")]
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=str(line_bot_api.get_insight_followers(t))))
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
        'Ocp-Apim-Subscription-Key': '6ac4b71081b84e3db81f589f774e956c',
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
        return json.dumps(r.json())

    except Exception as e:
        return str(e)


def get_reply(intent, score):
    if score < 0.8:
        return random.choice(unknown_msg)
    elif intent == "greet":
        return random.choice(greet_msg)
    elif intent == "greet_morning":
        return random.choice(greet_morning_msg)
    elif intent == "greet_afternoon":
        return random.choice(greet_afternoon_msg)
    elif intent == "greet_night":
        return random.choice(greet_night_msg)
    elif intent == "greet_bye":
        return random.choice(greet_bye_msg)
    elif intent == "time":
        return get_time()
    else:  # intent None
        return random.choice(unknown_msg)


if __name__ == '__main__':
    app.run()
