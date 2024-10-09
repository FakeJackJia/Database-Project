import redis, json
from flask import current_app
from models import News

class BaseRedisConnection(object):
    def __init__(self):
        redis_config = current_app.config['REDIS_SETTINGS']
        pool = redis.ConnectionPool(**redis_config)
        self.conn = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.conn.close()

    def delete(self, key):
        return self.conn.delete(key)

class NewsCache(BaseRedisConnection):
    def set_index_news(self):
        result = News.query.filter(News.is_valid==True, News.is_top==True).order_by(News.updated_at.desc()).all()
        news_list = [news.to_dict() for news in result]
        data = {"index_news_key":news_list}
        self.conn.set("index_news_key", json.dumps(data))

    def get_index_news(self):
        result = self.conn.get("index_news_key")

        if result is None:
            self.set_index_news()
            result = self.conn.get("index_news_key")

        news_info = json.loads(result)
        return news_info["index_news_key"]