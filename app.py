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
import requests
from urllib.parse import quote
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
from bs4 import BeautifulSoup

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('d0aa00b32ee8cb491e52dd801b86e041', None)
channel_access_token = os.getenv('xz/JtdLRqBocv4PpYboi0a0RnXv3vpurJW9ElUuaHPpT8DFAflJK1Fpwc4cy0Unl94BXTdCmVaWYB9g8v8G8hNeci/Kr45J3a9m7kHsbeXYGbmiDQltRp5dsLJj7aNr34uhp/iWf+B+fI4SUvFcd+AdB04t89/1O/w1cDnyilFU=', None)
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
        url = "http://b.hatena.ne.jp/hotentry?mode=rss"
        carousel_template = make_carousel(url)
        template_message = TemplateSendMessage(
            alt_text='人気エントリ', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text in ["social", "economics", "life", "knowledge",
                  "it", "fun", "entertainment", "game"]:
        url = f"http://b.hatena.ne.jp/hotentry/{text}.rss"
        carousel_template = make_carousel(url)
        template_message = TemplateSendMessage(
            alt_text='人気エントリ', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    else:
        text = quote(text)
        url = f"http://b.hatena.ne.jp/search/tag?q={text}&mode=rss"
        carousel_template = make_carousel(url)
        template_message = TemplateSendMessage(
            alt_text='人気エントリ', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)


def make_carousel(url):
    rss = feedparser.parse(url)
    bookmark_num_url = "http://api.b.st-hatena.com/entry.count?url="
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(
            thumbnail_image_url=BeautifulSoup(
                rss.entries[0].content[0]["value"], "html.parser")
            .find_all("img")[1]["src"].replace("http", "https"),
            text=rss.entries[0].summary[:60],
            title=rss.entries[0].title[:40],
            actions=[
                URITemplateAction(
                    label='Go to this page',
                    uri=rss.entries[0].link),
                URITemplateAction(
                    label=requests.get(
                        bookmark_num_url
                        + rss.entries[0].link).text + " bookmarks",
                    uri="http://b.hatena.ne.jp/entry/" + rss.entries[0].link,
                )]),
        CarouselColumn(
            thumbnail_image_url=BeautifulSoup(
                rss.entries[1].content[0]["value"], "html.parser")
            .find_all("img")[1]["src"].replace("http", "https"),
            text=rss.entries[1].summary[:60],
            title=rss.entries[1].title[:40],
            actions=[
                URITemplateAction(
                    label='Go to this page',
                    uri=rss.entries[1].link),
                URITemplateAction(
                    label=requests.get(
                        bookmark_num_url
                        + rss.entries[1].link).text + " bookmarks",
                    uri="http://b.hatena.ne.jp/entry/" + rss.entries[1].link,
                )]),
        CarouselColumn(
            thumbnail_image_url=BeautifulSoup(
                rss.entries[2].content[0]["value"], "html.parser")
            .find_all("img")[1]["src"].replace("http", "https"),
            text=rss.entries[2].summary[:60],
            title=rss.entries[2].title[:40],
            actions=[
                URITemplateAction(
                    label='Go to this page',
                    uri=rss.entries[2].link),
                URITemplateAction(
                    label=requests.get(
                        bookmark_num_url
                        + rss.entries[2].link).text + " bookmarks",
                    uri="http://b.hatena.ne.jp/entry/" + rss.entries[2].link,
                )]),
        CarouselColumn(
            thumbnail_image_url=BeautifulSoup(
                rss.entries[3].content[0]["value"], "html.parser")
            .find_all("img")[1]["src"].replace("http", "https"),
            text=rss.entries[3].summary[:60],
            title=rss.entries[3].title[:40],
            actions=[
                URITemplateAction(
                    label='Go to this page',
                    uri=rss.entries[3].link),
                URITemplateAction(
                    label=requests.get(
                        bookmark_num_url
                        + rss.entries[3].link).text + " bookmarks",
                    uri="http://b.hatena.ne.jp/entry/" + rss.entries[3].link,
                )]),
        CarouselColumn(
            thumbnail_image_url=BeautifulSoup(
                rss.entries[4].content[0]["value"], "html.parser")
            .find_all("img")[1]["src"].replace("http", "https"),
            text=rss.entries[4].summary[:60],
            title=rss.entries[4].title[:40],
            actions=[
                URITemplateAction(
                    label='Go to this page',
                    uri=rss.entries[4].link),
                URITemplateAction(
                    label=requests.get(
                        bookmark_num_url
                        + rss.entries[4].link).text + " bookmarks",
                    uri="http://b.hatena.ne.jp/entry/" + rss.entries[4].link,
                )]),


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
