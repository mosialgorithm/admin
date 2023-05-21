from persiantools.jdatetime import JalaliDateTime
from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import blog
from .models import News, NewsLike, Comment, Reply
from .forms import NewPostForm, NewsEditForm, CommentForm
from flask_login import login_user, logout_user, current_user
from utils import save_avatar, jdt_from_pdp, jdt_to_gregorian
from sqlalchemy.exc import IntegrityError
import pytz




@blog.route('/')
def index():
    all_news = News.query.order_by(News.created_at.desc()).all()
    sum_views = 0
    sum_likes = 0
    user_most_news = dict()
    news_most_seen = []
    news_most_liked = []
    news_most_comment = []
    user_write_news = []
    for news in all_news:
        if news.user_id not in user_write_news:
            user_write_news.append(news.user_id)
        if news.views > sum_views:
            sum_views = int(news.views)
            news_most_seen.clear()
            news_most_seen.append(news)
        if news.user_id not in user_most_news:
            user_most_news[news.user_id] = 1
        elif news.user_id in user_most_news:
            user_most_news[news.user_id] += 1     
    
    return render_template('blog/index.html',all_news=all_news, user_most_news=user_most_news, news_most_seen=news_most_seen)




@blog.route('/news-create', methods=['POST', 'GET'])
def news_create():
    form = NewPostForm()
    if request.method == 'POST':
        print('draft is : ',request.form.get('draft'))
        dt = jdt_to_gregorian(request.form.get('published_at'))
        if form.validate_on_submit():
            old_news = News.query.filter_by(title=request.form.get('title')).first()
            if old_news:
                flash(f'news by this title is exist, please change your title', 'danger')
                return redirect(url_for('blog.news_create'))
            news = News()
            news.user_id = current_user.id
            news.title = request.form.get('title')
            news.body = request.form.get('body')
            news.draft = 1 if request.form.get('draft') == 'y' else 0
            news.published_at = dt
            image = request.files.get('image')
            if image:
                save_avatar(image, news)
                news.image = f'uploads/{current_user.id}/{image.filename}'
            try:
                db.session.add(news)
                db.session.commit()
                flash('your new news is addedd successfully', 'success')
            except IntegrityError as er:
                flash(f'Error {er} is happened, please try again', 'warning')
            except Exception as e:
                flash(f'error {e} is happened, please try again', 'danger')
            finally:
                return redirect(url_for('blog.news_create', form=form))
        else:
            flash('form is not valid', 'danger')
            
    return render_template('/blog/news-create.html', form=form)


@blog.route('news-list', methods=['POST', 'GET'])
def news_list():
    page = request.args.get('page', default=1, type=int)
    news_all = News.query.order_by(News.created_at.desc()).all()
    all_news = News.query.order_by(News.created_at.desc()).paginate(page=page, per_page=7)
    for news in all_news:
        news.created_at  = JalaliDateTime.to_jalali(news.created_at)
        news.published_at  = JalaliDateTime.to_jalali(news.published_at)
    
    return render_template('blog/news-list.html',news_all=news_all, all_news=all_news, datetime=datetime)


@blog.route('news-edit/<int:news_id>', methods=['POST', 'GET'])
def news_edit(news_id):
    form = NewsEditForm()
    news = News.query.get_or_404(news_id)
    if request.method == 'POST':
        dt = jdt_to_gregorian(request.form.get('published_at'))
        if form.validate_on_submit():
            news.body = request.form.get('body')
            news.draft = 1 if request.form.get('draft') == 'y' else 0
            if news.published_at != request.form.get('published_at'):
                news.published_at = dt
            if news.image != request.files.get('image').filename:
                image = request.files.get('image')
                save_avatar(image, news)
                news.image = f'uploads/{current_user.id}/{image.filename}'
            try:
                db.session.add(news)
                db.session.commit()
                flash('your news is editted successfully', 'success')
            except IntegrityError as er:
                flash(f'Error {er} is happened, please try again', 'warning')
            except Exception as e:
                flash(f'error {e} is happened, please try again', 'danger')
            finally:
                return redirect(url_for('blog.news_edit',news_id=news.id, form=form))
        else:
            flash('form is not validated', 'danger')
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('blog.news_edit',news_id=news.id, form=form))

    form.body.data = news.body
    return render_template('blog/news-edit.html', news=news, form=form)


@blog.route('news-delete/<int:news_id>')
def news_delete(news_id):
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    
    return redirect(url_for('blog.news_list'))


@blog.route('news-draft/<int:news_id>')
def news_draft(news_id):
    news = News.query.get_or_404(news_id)
    # referrer = request.referrer.split('=')[-1]
    referrer = request.referrer
    print('request referrer',referrer)
    if news.draft == 0:
        news.draft = 1
        db.session.add(news)
        db.session.commit()
    else:
        
        news.draft = 0
        # news.published_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        news.published_at = datetime.now()
        # news.published_at = jdt_from_pdp(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # news.published_at = datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        # news.published_at = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
        print('/'*50)
        # print(datetime(news.published_at))
        print('/'*50)
        db.session.add(news)
        db.session.commit()
    return redirect(f'{referrer}')
               
        
@blog.route('news-detail/<int:news_id>/<string:news_slug>')
def news_detail(news_id, news_slug):
    form = CommentForm()
    news = News.query.get_or_404(news_id)
    news.views += 1
    db.session.add(news)
    db.session.commit()
    print(news)
    lst = []
    for ns in news.users_like:
        lst.append(ns.user_id)
        
    return render_template('blog/news-detail.html', form=form, news=news, lst=lst)


@blog.route('news-like/<int:news_id>/<int:user_id>')
def news_like(news_id, user_id):
    user = NewsLike.query.filter_by(news_id=news_id, user_id=current_user.id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'you dislikes news', 'warning')
    else:
        news_like = NewsLike()
        news_like.user_id = user_id
        news_like.news_id = news_id
        news = News.query.get(news_id)
        db.session.add(news_like)
        db.session.commit()
        flash(f'you likes news {news.title}', 'success')
    return redirect(request.referrer)
    


@blog.route('send-comment/<int:news_id>', methods=['POST'])
def send_comment(news_id):
    form = CommentForm()
    news = News.query.get_or_404(news_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment()
            comment.title = request.form.get('title')
            comment.user_id = current_user.id
            comment.news_id = news_id
            try:
                db.session.add(comment)
                db.session.commit()
                flash(f'your comment for news {news.title} is saved', 'success')
            except IntegrityError as ie:
                db.session.rollback()
                flash(f'error {ie} is happened, please try again', 'danger')
            except Exception as e:
                flash(f'error {e} is happened !!, please try again', 'danger')
            finally:
                return redirect(request.referrer)
    return redirect(request.referrer)
    
    
    
@blog.route('send-reply/<int:news_id>/<int:comment_id>', methods=['POST'])
def send_reply(news_id, comment_id):
    form = CommentForm()
    comment = Comment.query.get_or_404(comment_id)
    if request.method == 'POST' and form.validate_on_submit():
        reply = Reply()
        reply.title = request.form.get('title')
        reply.news_id = news_id
        reply.comment_id = comment_id
        reply.user_id = current_user.id 
        try:
            db.session.add(reply)
            db.session.commit()
            flash(f'your comment for comment {comment.title} is saved', 'success')
        except IntegrityError as ie:
            db.session.rollback()
            flash(f'error {ie} is happened, please try again', 'danger')
        except Exception as e:
            flash(f'error {e} is happened !!, please try again', 'danger')
        finally:
            return redirect(request.referrer)
    return redirect(request.referrer)
        
    

@blog.route('news-all')
def news_all():
    news_all = News.query.filter_by(draft=0).order_by(News.created_at.desc()).all()
    print('9'*50)
    for news in news_all:
        print(news.created_at, news.title)
    print('9'*50)
    # most_views = news_all.order_by(News.view)[1]
    sum = 0
    most_view = []
    for news in news_all:
        if news.views > sum:
            sum = int(news.views)
            most_view.clear()
            most_view.append(news)
    print(sum)
    print(most_view)
            
    
    return render_template('blog/news-all.html', news_all=news_all, most_view=most_view)


