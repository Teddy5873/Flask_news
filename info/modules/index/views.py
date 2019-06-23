from flask import current_app, session
from flask import render_template

from info import redis_store, constants
from info.models import User, News
from . import index_blu


@index_blu.route('/')
def index():
    user_id = session.get("user_id",None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    news_list = None
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in news_list if news_list else[]:
        click_news_list.append(news.to_basic_dict())


    data = {
        "user":user.to_dict() if user else None,
        "click_news_list": click_news_list,
    }
    return render_template('news/index.html',data=data)



# 在打开网页的时候，浏览器会默认去请求根路径+favicon.ico作网站标签的小图标
# send_static_file 是 flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
