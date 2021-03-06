import json
from json import JSONDecodeError
import random
import requests
import sys
import datetime
import pytz
import gotcha
from flask import Flask, request, abort, send_from_directory
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# const key
line_bot_api = LineBotApi('uJ6LnR2TWpOmYqSYW9yg1nSe1GO9+c3euzndfcjTeTSlfz1r58dfBxpnNySHjq7/oUAmiO0VBDHb5HyLSdnu+PXMA71HJkbT4jwqfTDXhpXRAWOFsEVbpjbDNahvbXVLVh9cZsTLH+yB3cxwMsyC/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('905c2e3f57145acb7d791c46dec9a573')
iotpath = "kkgmsmepoa54fd9rew2da/2n11td"
iotkey = "a43fdfvvpefd55"
base = "https://joejoe2.github.io/LineBot/"

gotcha_list = []

# const reply
unknown_msg = ["我聽不懂", "請用更具體的命令", "我不明白，請說清楚一點"]
greet_msg = ["你好", "哈囉", "嗨~"]
greet_morning_msg = ["早安", "早", "早上好"]
greet_afternoon_msg = ["午安", "下午好"]
greet_night_msg = ["晚安"]
greet_bye_msg = ["再見", "掰掰", "下次見"]

# setup flask
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))


@app.route('/')
def index():
    return "<p>Hello World!" + "<br>" + get_time(sep="<br>") + "</p>"


@app.route("/callback", methods=['POST'])
def callback():
    """
    bot webhook endpoint
    """
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


@app.route("/broadcast", methods=['GET'])
def broadcast():
    """
        broadcast msg endpoint
        ,receive by get     /broadcast?data=
    """
    body = request.args.get("data")
    line_bot_api.broadcast(TextSendMessage(text="test broadcast push : "+str(body)))
    # print(body)
    return "broadcast data = " + body + " complete !"


@app.route("/push", methods=['GET'])
def push():
    """
            push msg endpoint to a specific user
            ,receive by get     /push?id=...&data=...        """
    uid = request.args.get("id")
    body = request.args.get("data")

    try:
        line_bot_api.push_message(str(uid), TextSendMessage(text=str(body)))
    except Exception as ex:
        print(ex)
        return str(ex)

    return 'push to id = ' + uid + " data = " + body + " complete !"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    """
        handle different kinds of input or cmd
    """
    if event.source.type == "group":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="join group: "+event.source.group_id))
        return
        pass

    text: str = event.message.text
    user_id = event.source.user_id
    print(user_id)
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    pic_url = profile.picture_url
    status = profile.status_message

    if text.lower().startswith("[gotcha]"):  # cmd gotcha
        # each user has a gotcha machine
        gotcha_m = None
        for g in gotcha_list:
            if g.id == user_id:
                gotcha_m = g
                break
            pass
        if gotcha_m == None:
            gotcha_m = gotcha.gotcha(user_id, base)
            gotcha_list.append(gotcha_m)
            pass

        if text.find("star5") >= 0:  # 5* only state
            r = gotcha_m.enters5()
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=r[1]), ImageSendMessage(r[0], r[0])])
            pass
        elif text.find("star4") >= 0:  # 4* only state
            r = gotcha_m.enters4()
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=r[1]), ImageSendMessage(r[0], r[0])])
            pass
        elif text.find("star3") >= 0:  # 3* only state
            r = gotcha_m.enters3()
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=r[1]), ImageSendMessage(r[0], r[0])])
            pass
        elif text.find("10") >= 0:  # state10 (pick 10*default sate)
            res = gotcha_m.pick10()
            for r in res:
                line_bot_api.push_message(str(user_id), [TextSendMessage(text=r[1]), ImageSendMessage(r[0], r[0])])
            pass
        elif text.find("event") >= 0:  # event only state
            r = gotcha_m.enterevent()
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=r[1]), ImageSendMessage(r[0], r[0])])
            pass
        elif text.find("show") >= 0:  # show statistic
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=gotcha_m.show()))
            pass
        elif text.find("fsm") >= 0:  # show fsm
            line_bot_api.reply_message(event.reply_token, [ImageSendMessage(base+"fsm1.png", base+"fsm1.png"), ImageSendMessage(base+"fsm2.png", base+"fsm2.png")])
            pass
        else:  # default state
            r = gotcha_m.enterdefault()
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=r[1]), ImageSendMessage(r[0], r[0])])
            pass
        pass
    elif text.lower().startswith("[time]") or text.startswith("[時間]"):  # cmd time
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=get_time("\n")))
    elif text.startswith("[luis]"):  # cmd luis
        send_text = get_luis(text.replace("[luis]", ""))
        reply = ""
        try:
            obj = json.loads(send_text)
            # format example
            # {"query": "\u65e9\u5348\u665a", "topScoringIntent":
            # {"intent": "greet_morning", "score": 0.730086446}, "entities": []}
            # reply is based on luis intent and score
            reply = get_reply(obj["topScoringIntent"]["intent"], obj["topScoringIntent"]["score"])
        except JSONDecodeError as ex:
            print(ex.msg)

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=send_text+"\n"+reply))
    elif text.startswith("[my info]"):  # cmd to check user's info
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="id : " + user_id + "\n" + "name : " + user_name))
    elif text.startswith("[followers]"):  # cmd to show bot's followers num
        t = text[text.find("{")+1:text.find("}")]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(line_bot_api.get_insight_followers(t))))
    else:  # if input does not belongs to anyone above, just say same back
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_name + " say : " + text))


def get_time(sep="\n"):
    """
    get time in some useful timezone to me

    :param sep:  separator
    :return:  time in string
    """
    d1 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Taipei"))
    d2 = datetime.datetime.now().astimezone(pytz.timezone("Asia/Tokyo"))
    d3 = datetime.datetime.now().astimezone(pytz.timezone("America/Los_Angeles"))
    return "Taiwan : "+str(d1)+sep+"Japan : "+str(d2)+sep+"Los_Angeles : "+str(d3)


def get_luis(text):
    """
    query input text into some simple intent class(ex time, greeting ...) and make a reply based on azure luis service

    :param text: query string
    :return: json with intent and score
    """
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
    """
    based on intent and score, choose a different reply

    :param intent:string
    :param score:flaot
    :return reply:string
    """
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


@app.route('/'+iotpath, methods=['POST'])
def iotentry():
    """
    for iot status push broadcast test

    :return: push broadcast result
    """
    msg = request.args.get("msg")
    key = request.args.get("k")
    uid = request.args.get("id")
    if key == iotkey:
        try:
            line_bot_api.push_message(str(uid), TextSendMessage(text=str(msg)))
        except Exception as ex:
            print(ex)
        return "iot push " + msg + " complete !"
    else:
        return "access denied"


@app.route('/getfsm', methods=['GET'])
def getfsm():
    """
    callback for downloading fsm1 or 2 .png

    :return:  .png file
    """
    f = request.args.get("f")
    f = "fsm2.png" if f == '2' else "fsm1.png"
    try:
        return send_from_directory('', f, as_attachment=True, attachment_filename=f)
    except Exception as e:
        return str(e)
    pass


if __name__ == '__main__':  # run app
    app.run(host="0.0.0.0", port=port, debug=True)
