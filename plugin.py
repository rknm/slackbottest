from slackbot.bot import respond_to
from slackbot.bot import default_reply
from tinydb import TinyDB, Query
import json
from datetime import date
import update

url=''
dbpath=''

@respond_to('show deleted item')
def showdeleteditem(message):
    db = TinyDBd(bpath)
    q = Query()
    items = db.search(q.itemstate == 'deleted')
    message.reply(date.today().strftime('%Y/%m/%d')+'に削除されたアイテムは'+str(len(items))+'件です')
    db.close()

@respond_to('show update item')
def showupdateitem(message):
    db = TinyDB(dbpath)
    q = Query()
    items = db.search(q.itemstate == 'update')
    message.reply(date.today().strftime('%Y/%m/%d')+'に更新されたアイテムは'+str(len(items))+'件です')
    db.close()

@respond_to('show new item')
def shownewitem(message):
    db = TinyDB(dbpath)
    q = Query()
    items = db.search(q.itemstate == 'new')
    message.reply(date.today().strftime('%Y/%m/%d')+'に追加されたアイテムは'+str(len(items))+'件です')
    for item in items:
        # 商品名と価格とurlをリプライする
        mess = item.get('itemname') + '\n'
        mess += item.get('nosalevalue')+'->'+'`'+item.get('salevalue')+'`\n'
        mess += item.get('imageurl') + '\n'
        mess += farfetchurl + item.get('itemurl')+'\n'
        message.reply(mess)
    db.close()

@respond_to('updateinfo')
def updateinfo(message):
    updatedb()
    message.reply('データ更新完了！')
