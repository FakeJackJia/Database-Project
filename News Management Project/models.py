from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from mongoengine.fields import IntField, StringField, BooleanField, ObjectIdField, DateTimeField

db = SQLAlchemy()
mongodb = MongoEngine()

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='主题')
    img_url = db.Column(db.String(200), nullable=False, comment='主图地址')
    content = db.Column(db.String(2000), nullable=False, comment='新闻内容')
    is_valid = db.Column(db.Boolean, default=True, comment='逻辑删除')
    is_top = db.Column(db.Boolean, default=True, comment='是否置顶')
    created_at = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now(), comment='最后修改时间')
    news_type = db.Column(db.Enum('本地', '百家', '娱乐', '军事'), comment='新闻类别')

    def get_comments(self):
        comments = Comments.objects.filter(object_id=self.id, is_valid=True)
        return comments

    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'img_url':self.img_url,
            'content':self.content,
            'news_type':self.news_type,
            'created_at':self.created_at.strftime('%Y-%m-%d')
        }

class Comments(mongodb.Document):
    object_id = IntField(required=True, verbose_name='评论的新闻')
    content = StringField(required=True, max_length=2000, verbose_name='评论的内容')
    is_valid = BooleanField(default=True, verbose_name='逻辑删除')
    reply_id = ObjectIdField(verbose_name='回复评论的ID')
    created_at = DateTimeField(default=datetime.now(), verbose_name='创建时间')
    updated_at = DateTimeField(default=datetime.now(), verbose_name='最后修改时间')

    meta = {
        'collection':'comments',
        'ordering':['is_valid', '-created_at']
    }

    @property
    def news_obj(self):
        return News.query.get(self.object_id)

    def __str__(self):
        return f'Comments: {self.content}'