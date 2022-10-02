from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import MessageEvent, TextMessage

import settings
from smartbrain.smartbrain import SmartBrain
from imagedata.imagedata import ImageData
from imageTexter.imageTexter import ImageTexter
from bot import Bot
from mock import create_mock_event


# 初始化
app = Flask(__name__)
DEBUG = False

bot = Bot(settings.LINE_API)
handler = WebhookHandler(settings.LINE_HANDLE)

image_fetcher = ImageData()
image_texter = ImageTexter()
smart_brainer = SmartBrain()


@app.route('/line-webhook', methods=['POST'])
def callback():
    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    if settings.LOCAL_DEBUG:
        handle_debug_request(body)
    else:
        try:
            # get X-Line-Signature header value
            signature = request.headers['X-Line-Signature']
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_line_request(event):
    handle_message(event)


def handle_debug_request(body):
    handle_message(create_mock_event(body))


def handle_message(event):
    print(event.source)
    print('{}: {}'.format(event.message.id, event.message.text))

    # 過濾及初始化訊息
    is_moonshine_group = False
    if event.source.type == 'group':
        is_moonshine_group = event.source.group_id == settings.MOONSHINE_CHANNEL

    msg = event.message.text
    token = event.reply_token

    # 罐頭訊息
    if msg in settings.reaction:
        content = settings.reaction[msg]
        bot.reply(token, content)
    # 圖庫訊息
    elif msg == '抽同事':
        url = image_fetcher.get_image_url('faces')
        bot.reply(token, url)

    elif msg == '抽':
        url = image_fetcher.get_image_url('beauty')
        bot.reply(token, url)

    elif msg == '奶':
        url = image_fetcher.get_image_url('boob')
        bot.reply(token, url)

    elif msg == '老外' and not is_moonshine_group:
        url = image_fetcher.get_image_url('Reddit')
        bot.reply(token, url)

    # 產生LOL圖片
    elif msg.lower() == '夢想lol':
        url = image_texter.draw_lol()
        bot.reply(token, url)

    # 產生梗圖
    elif msg.startswith('夢想'):
        texts = msg.split()
        if 1 < len(texts) < 4 and texts[0] != '夢想':
            source = texts.pop(0)[2:]
            if source != '':
                url = image_texter.generate(source, texts)
                if url:
                    bot.reply(token, url)

    # 問題
    elif msg.startswith('里長'):
        result = smart_brainer.detect(msg)
        if result:
            bot.reply(token, result)


if __name__ == '__main__':
    DEBUG = True
    app.run(debug=True)
