from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

NEWS_TYPE_CHOICES = (
    ('本地', '本地'),
    ('百家', '百家'),
    ('军事', '军事'),
    ('娱乐', '娱乐')
)

class NewsForm(FlaskForm):
    title = StringField(label='新闻标题', description='请输入标题',
                        validators=[DataRequired('请输入标题'), Length(min=10, max=200, message='新闻标题的长度在20-200之间')],
                        render_kw={"class": "form-control"})
    content = TextAreaField(label='新闻内容', description='请输入内容',
                            validators=[DataRequired('请输入内容'), Length(min=50, message='新闻标题的长度要在50以上')],
                            render_kw={"claas":"control", "rows":5})
    news_type = SelectField(label='新闻类型', choices=NEWS_TYPE_CHOICES,
                            render_kw={'class':'form-control'})
    img_url = StringField(label='新闻图片', description='请输入图片地址',
                          default='/static/img/news/new1.jpg',
                          render_kw={'required':'required', 'class':'form-control'})
    is_top = BooleanField(label='是否置顶')
    submit = SubmitField(label='提交', render_kw={'class':'btn btn-info'})

class CommentForm(FlaskForm):
    object_id = HiddenField(label='关联的新闻', validators=[DataRequired("新闻ID不能为空")])
    reply_id = HiddenField(label='关联的回复')
    content = TextAreaField(label='评论的内容', validators=[DataRequired("请输入内容"),
                            Length(min=5, max=200, message="评论内容在5-200之间")],
                            description="请输入内容", render_kw={'class':'form-control', 'rows':5})
    submit = SubmitField(label='提交评论', render_kw={'class': 'btn btn-info'})