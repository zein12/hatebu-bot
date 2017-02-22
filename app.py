# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
import feedparser
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
parser = WebhookParser(channel_secret)


@app.route('/')
def hello_world():
    return 'Hello World!'


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if text == "all":
        rss = feedparser.parse("http://b.hatena.ne.jp/hotentry?mode=rss")
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text=rss.entries[0].link, title=rss.entries[0].title, actions=[
                URITemplateAction(label='Go to this page',
                                  uri=rss.entries[0].link)]),
            CarouselColumn(text=rss.entries[1].link, title=rss.entries[1].title, actions=[
                URITemplateAction(label='Go to this page',
                                  uri=rss.entries[1].link)]),
            CarouselColumn(text=rss.entries[2].link, title=rss.entries[2].title, actions=[
                URITemplateAction(label='Go to this page',
                                  uri=rss.entries[2].link)]),

        ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text in ["social", "economics", "life", "knowledge", "it", "fun", "entertainment", "game"]:
        pass
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))


def generate_carousel(rss):
    print("generate_carousel called")
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(text=rss.entries[0].link,
                       title=rss.entries[0].title,
                       actions=[URITemplateAction(label='Go to this page',
                                                  uri=rss.entries[0].link)]),
        CarouselColumn(text=rss.entries[1].link,
                       title=rss.entries[1].title,
                       actions=[URITemplateAction(label='Go to this page',
                                                  uri=rss.entries[1].link)]),
        CarouselColumn(text=rss.entries[2].link,
                       title=rss.entries[2].title,
                       actions=[URITemplateAction(label='Go to this page',
                                                  uri=rss.entries[2].link)]),
        CarouselColumn(text=rss.entries[3].link,
                       title=rss.entries[3].title,
                       actions=[URITemplateAction(label='Go to this page',
                                                  uri=rss.entries[3].link)]),
        CarouselColumn(text=rss.entries[4].link,
                       title=rss.entries[4].title,
                       actions=[URITemplateAction(label='Go to this page',
                                                  uri=rss.entries[4].link)]),
    ])
    return carousel_template


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
