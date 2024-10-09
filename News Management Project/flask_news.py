from datetime import datetime
from flask import Flask, render_template, abort, redirect, flash, request, url_for
from cache import NewsCache
from forms import NewsForm, CommentForm
from models import db, News, mongodb, Comments

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
mongodb.init_app(app)

@app.route('/')
def index():
    # main page
    cache_obj = NewsCache()
    news_list = cache_obj.get_index_news()
    return render_template('index.html', news_list=news_list)

@app.route('/cat/<news_type>')
def cat(news_type):
    news_list = News.query.filter(News.news_type == news_type, News.is_valid==True).all()
    return render_template('cat.html', news_list=news_list, news_type=news_type)

@app.route('/detail/<int:pk>')
def detail(pk):
    # news content
    news_obj = News.query.get(pk)
    form = CommentForm(data={'object_id':pk})
    # check whether news is deleted or not
    if news_obj is None or not news_obj.is_valid:
        abort(404)
    return render_template('detail.html', news_obj=news_obj, form=form)

@app.route('/admin')
@app.route('/admin/<int:page>')
def admin(page=1):
    # Backend management
    page_size = 3

    title = request.args.get('title', '')
    page_data = News.query.filter(News.is_valid == True)
    if title:
        page_data = page_data.filter(News.title.contains(title))

    page_data = page_data.paginate(page=page, per_page=page_size)
    return render_template('admin/index.html', page_data=page_data, title=title)

@app.route('/admin/news/add', methods=['GET', 'POST'])
def news_add():
    form = NewsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            news_obj = News(
                title=form.title.data,
                content=form.content.data,
                img_url=form.img_url.data,
                is_top=form.is_top.data,
                news_type=form.news_type.data
            )

            db.session.add(news_obj)
            db.session.commit()

            # cache top news
            if news_obj.is_top:
                cache_obj = NewsCache()
                cache_obj.set_index_news()

            flash('新增成功', 'success')
            return redirect('/admin')
        else:
            flash('添加失败', 'danger')

    return render_template('admin/add.html', form=form)

@app.route('/admin/news/update/<int:pk>', methods=['GET', 'POST'])
def news_update(pk):
    news_obj = News.query.get(pk)
    if not news_obj.is_valid:
        abort(404)

    form = NewsForm(obj=news_obj)
    is_top_origin = news_obj.is_top
    if request.method == 'POST':
        if form.validate_on_submit():
            is_top = form.is_top.data
            news_obj.title = form.title.data
            news_obj.content = form.content.data
            news_obj.img_url = form.img_url.data
            news_obj.news_type = form.news_type.data
            news_obj.is_top = is_top
            news_obj.updated_at = datetime.now()
            db.session.add(news_obj)
            db.session.commit()

            # update cache
            if is_top != is_top_origin:
                cache_obj = NewsCache()
                cache_obj.set_index_news()

            flash('修改成功', 'success')
            return redirect('/admin')
        else:
            flash('修改失败', 'danger')

    return render_template('admin/update.html', form=form)

@app.route('/admin/news/delete/<int:pk>', methods=['POST'])
def news_delete(pk):
    news_obj = News.query.get(pk)
    if news_obj is None or not news_obj.is_valid:
        return 'no'
    news_obj.is_valid = False

    # update cache
    if news_obj.is_top:
        cache_obj = NewsCache()
        cache_obj.set_index_news()

    db.session.add(news_obj)
    db.session.commit()
    return 'yes'

@app.route('/comment/<int:news_id>/add', methods=['POST'])
def comment_add(news_id):
    news_obj = News.query.get(news_id)
    form = CommentForm(data={'object_id':news_id})
    if request.method == 'POST':
        if form.validate_on_submit():
            comment_obj = Comments(
                content=form.content.data,
                object_id=news_id
            )
            reply_id = form.reply_id.data
            if reply_id:
                comment_obj.reply_id = reply_id
            comment_obj.save()
            flash('评论成功', 'success')
            return redirect(url_for('detail', pk=news_id))
        else:
            flash('评论失败', 'danger')

    return render_template('detail.html', form=form, news_obj=news_obj)

@app.route('/admin/comment')
@app.route('/admin/comment/<int:page>')
def admin_comment(page=1):
    page_size=5
    content = request.args.get('content', '')
    if content:
        page_data = Comments.objects.filter(content__contains=content)
    else:
        page_data = Comments.objects.all()
    page_data = page_data.paginate(page=page, per_page=page_size)
    return render_template('admin/comments.html', page_data=page_data, content=content)

@app.route('/admin/comment/delete/<string:pk>', methods=['POST'])
def comment_delete(pk):
    comment_obj = Comments.objects.filter(id=pk).first()
    if comment_obj is None or not comment_obj.is_valid:
        return 'no'
    comment_obj.is_valid = False
    comment_obj.save()
    return 'yes'

if __name__ == '__main__':
    # create table
    # with app.app_context():
    #     db.create_all()

    app.run()