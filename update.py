from urllib.request import urlopen
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

# updateDB
# check website and update db
def updatedb() :
    db = TinyDB('db path')
    q = Query()
    ITEM_NAME = 'itemname'
    NO_SALE_VALUE = 'nosalevalue'
    SALE_VALUE = 'salevalue'
    ITEM_URL = 'itemurl'
    IMAGE_URL = 'imageurl'
    UPDATE_FLAG = 'updateflag'
    NEW_ITEM_FLAG = 'newitemflag'
    ITEM_STATE = 'itemstate'

    STATE_NEW = 'new'
    STATE_UPDATE = 'update'
    STATE_NO_CHANGE = 'nochange'
    STATE_DELETED = 'deleted'

    html = urlopen('site url')
    bsObj = BeautifulSoup(html, "html.parser")
    # change flag
    # no update item is NO_CHANGE
    db.update({ITEM_STATE:STATE_DELETED}, q.itemstate == STATE_NEW)
    db.update({ITEM_STATE:STATE_DELETED}, q.itemstate == STATE_UPDATE)
    db.update({ITEM_STATE:STATE_DELETED}, q.itemstate == STATE_NO_CHANGE)
    articles = bsObj.findAll('article', {'itemtype':'url'})
    for article in articles:
        # get a tag
        iteminfo = article.findAll('a', {'class':'listing-item-content listing-item-link no-underline'})[0]
        # get item name
        itemname = iteminfo.p.string
        # get div tag
        valuediv = iteminfo.findAll('div', {'class':'listing-item-contentSale'})[0]
        # get no sale value
        nosalevalue = valuediv.findAll('span')[0].string
        # get sale value
        salevalue = valuediv.findAll('span')[2].string
        # get div tag
        imgdiv = article.findAll('div', {'class':'listing-item-image'})[0]
        itemurl = imgdiv.a.get('href')
        imageurl = imgdiv.a.img.get('data-img')

        #
        elem = db.search(q.imageurl == imageurl)
        if (len(elem) == 0):
            # データベースに登録されていない場合はデータベースに登録する
            db.insert({ITEM_NAME:itemname, NO_SALE_VALUE:nosalevalue, SALE_VALUE:salevalue, ITEM_URL:itemurl, IMAGE_URL:imageurl, ITEM_STATE:STATE_NEW})
        elif(len(elem) == 1):
            # データベースに登録されている場合
            # 値段に変更がないかをチェックする
            if(elem[0].get(SALE_VALUE) != salevalue):
                # 一致しない場合はデータを更新する
                # imageurlに一致するデータの値を更新する
                db.update({SALE_VALUE:salevalue}, q.imageurl == imageurl)
                # 状態を更新済みに変更する
                db.update({ITEM_STATE:STATE_UPDATE}, q.imageurl == imageurl)
            else:
                # 状態を存在するに変更する
                db.update({ITEM_STATE:STATE_NO_CHANGE}, q.imageurl == imageurl)

    db.close()

updatedb()
