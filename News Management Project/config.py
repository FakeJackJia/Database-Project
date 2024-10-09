from urllib.parse import quote_plus

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:%s@localhost/flask_news' % quote_plus('PASSWORD')
    SECRET_KEY = '123123'
    MONGODB_SETTINGS = {'db': 'flask_news'}
    REDIS_SETTINGS = {
        'host':'localhost',
        'port':6379,
        'db':2,
        'max_connections':20,
        'decode_responses':True
    }