# Hatebu-bot

Sample hatena-bookmark-bot using [Flask](http://flask.pocoo.org/) and [Line bot sdk](https://github.com/line/line-bot-sdk-python)


## Getting started

```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN

$ pip install -r requirements.txt
```

## Useage

### All popular entries
To see all category, sent "all"

### Category view
To see by category sent text as follows

- social … 世の中
- economics … 政治と経済
- life … 暮らし
- knowledge … 学び
- it … テクノロジー
- fun … おもしろ
- entertainment … エンタメ
- game … アニメとゲーム

### Search by keywords

If you sent text expect for above, you can search by using that word.
