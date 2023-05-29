from persiantools.jdatetime import JalaliDateTime, digits
from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import blog
from .models import News, NewsLike, Comment, Reply, Category
from .forms import NewPostForm, NewsEditForm, CommentForm
from flask_login import login_user, logout_user, current_user
from utils import save_avatar, jdt_from_pdp, jdt_to_gregorian
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from collections import Counter
from auth.models import User, UserLogs




# News Function
@blog.route('/')
def index():
    """blog home page"""
    news_most_seen = News.query.order_by(News.views.desc()).all()
    # ==================================================================
    # sum_of_views_by_draft = News.query.with_entities(News.draft).all()
    # ==================================================================
    # sum_of_views_by_draft = News.query.with_entities(News.draft, News.created_at).all()

    user_most_news = []
    for news in news_most_seen:
        # user_most_news.append((news.user_id, news.views))
        user_most_news.append(news.user_id)
    
    user_most_news_count = dict(Counter(user_most_news))
    
    user_log = UserLogs.query.filter_by(user_id=current_user.id).all()
    print('-------------user_log-----------')
    for user in user_log:
        print(user)
    print('-'*50)
    return render_template('blog/index.html',all_news=news_most_seen,
                           news_most_seen=news_most_seen,
                           user_most_news_count=user_most_news_count,
                           User=User)


@blog.route('/news-create', methods=['POST', 'GET'])
def news_create():
    """create news in blog app"""
    form = NewPostForm()
    categories = Category.query.all()
    form.category.choices = [(cat.id, cat.title) for cat in categories]
    if request.method == 'POST':
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
            if datetime.now() < dt:
                news.draft = 1
                flash('your news be draft, because your publish time is not now', 'warning')
            news.published_at = dt
            news.categories = [Category.query.get(category_id) for category_id in form.category.data]
            image = request.files.get('image')
            if image:
                save_avatar(image, news)
                news.image = f'uploads/{current_user.id}/{image.filename}'
            try:
                db.session.add(news)
                db.session.commit()
                # ========= event logging ==============
                event = UserLogs()
                event.save_log(current_user.id,news_create.__doc__,news)
                # ========= end of event logging========
                flash('your new news is addedd successfully', 'success')
            except IntegrityError as er:
                flash(f'Error {er} is happened, please try again', 'warning')
            except Exception as e:
                flash(f'error {e} is happened, please try again', 'danger')
            finally:
                return redirect(url_for('blog.news_create', form=form))
        else:
            flash('form is not valid', 'danger')
    # categories = Category.query.order_by(Category.id.asc()).all()
    # form.categories.choices = [(category.id, category.name) for category in categories]
    
    
        
    return render_template('/blog/news-create.html', form=form)


@blog.route('news-list', methods=['POST', 'GET'])
def news_list():
    """showing all news for superuser"""
    page = request.args.get('page', default=1, type=int)
    news_all = News.query.order_by(News.created_at.desc()).all()
    all_news = News.query.order_by(News.created_at.desc()).paginate(page=page, per_page=7)
    today = datetime.today()
    
    return render_template('blog/news-list.html',news_all=news_all, all_news=all_news, today=today, JalaliDateTime=JalaliDateTime)


@blog.route('news-edit/<int:news_id>', methods=['POST', 'GET'])
def news_edit(news_id):
    """editing news in blog app"""
    form = NewsEditForm()
    categories = Category.query.all()
    form.category.choices = [(cat.id, cat.title) for cat in categories]
    news = News.query.get_or_404(news_id)
    if request.method == 'POST':
        dt = jdt_to_gregorian(request.form.get('published_at'))
        if form.validate_on_submit():
            news.body = request.form.get('body')
            news.categories = [Category.query.get(category_id) for category_id in form.category.data]
            news.draft = 1 if request.form.get('draft') == 'y' else 0
            if news.published_at != request.form.get('published_at'):
                news.published_at = dt
            if datetime.now() < dt:
                news.draft = 1
                flash('your news be draft, because your publish time is not now', 'warning')
            if news.image != request.files.get('image').filename:
                image = request.files.get('image')
                save_avatar(image, news)
                news.image = f'uploads/{current_user.id}/{image.filename}'
            try:
                db.session.add(news)
                db.session.commit()
                # ========= event logging ==============
                event = UserLogs()
                event.save_log(current_user.id,news_edit.__doc__,news)
                # ========= end of event logging========
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
    form.category.data = [category.id for category in news.categories]
    return render_template('blog/news-edit.html', news=news, form=form)


@blog.route('news-delete/<int:news_id>')
def news_delete(news_id):
    """deleting news in blog app"""
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    # ========= event logging ==============
    event = UserLogs()
    event.save_log(current_user.id,news_delete.__doc__,news)
    # ========= end of event logging========
    
    return redirect(url_for('blog.news_list'))


@blog.route('news-draft/<int:news_id>')
def news_draft(news_id):
    """changing draft for show or hide news"""
    news = News.query.get_or_404(news_id)
    # referrer = request.referrer.split('=')[-1]
    referrer = request.referrer
    print('request referrer',referrer)
    if news.draft == 0:
        news.draft = 1
        db.session.add(news)
        db.session.commit()
        # ========= event logging ==============
        event = UserLogs()
        event.save_log(current_user.id,news_draft.__doc__,news)
        # ========= end of event logging========
    else:
        news.draft = 0
        news.published_at = datetime.now()
        db.session.add(news)
        db.session.commit()
        # ========= event logging ==============
        event = UserLogs()
        event.save_log(current_user.id,news_draft.__doc__,news)
        # ========= end of event logging========
    return redirect(f'{referrer}')
               
        
@blog.route('news-detail/<int:news_id>/<string:news_slug>')
def news_detail(news_id, news_slug):
    """show detail of a news"""
    form = CommentForm()
    news = News.query.get_or_404(news_id)
    news.views += 1
    db.session.add(news)
    db.session.commit()
    lst = []
    for ns in news.users_like:
        lst.append(ns.user_id)
        
    return render_template('blog/news-detail.html', form=form, news=news, lst=lst)


@blog.route('news-like/<int:news_id>/<int:user_id>')
def news_like(news_id, user_id):
    """like a news in blog app"""
    user = NewsLike.query.filter_by(news_id=news_id, user_id=current_user.id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        # ========= event logging ==============
        event = UserLogs()
        event.save_log(current_user.id, "news unliked", user) # why dont work news_like.__doc__ ????????????
        # ========= end of event logging========
        flash(f'you dislikes news', 'warning')
    else:
        news_like = NewsLike()
        news_like.user_id = user_id
        news_like.news_id = news_id
        news = News.query.get(news_id)
        db.session.add(news_like)
        db.session.commit()
        # ========= event logging ==============
        event = UserLogs()
        event.save_log(current_user.id, "news liked", news_like) # why dont work news_like.__doc__ ????????????
        # ========= end of event logging========
        flash(f'you likes news {news.title}', 'success')
    return redirect(request.referrer)


@blog.route('news-all')
def news_all():
    """showing all news for all users"""
    news_all = News.query.filter_by(draft=0).order_by(News.created_at.desc()).all()
    for news in news_all:
        if news.published_at <= datetime.now():
            news.draft = False
            db.session.add(news)
            db.session.commit()
            # ========= event logging ==============
            event = UserLogs()
            event.save_log(current_user.id,news_all.__doc__,news)
            # ========= end of event logging========
    sum = 0
    most_view = []
    for news in news_all:
        if news.views > sum:
            sum = int(news.views)
            most_view.clear()
            most_view.append(news)
            
    return render_template('blog/news-all.html', news_all=news_all, most_view=most_view)


@blog.route('news-draft-list')
def news_draft_list():
    """showing all news that draft is True"""
    page = request.args.get('page', default=1, type=int)
    all_news = News.query.filter_by(draft=1).order_by(News.created_at.desc()).paginate(page=page, per_page=7)
    for news in all_news:
        news.created_at  = JalaliDateTime.to_jalali(news.created_at)
        news.published_at  = JalaliDateTime.to_jalali(news.published_at)
    
    return render_template('blog/news-draft.html', all_news=all_news, datetime=datetime)

# =============================================== Comment Function ==========================================
@blog.route('send-comment/<int:news_id>', methods=['POST'])
def send_comment(news_id):
    """user send comment in blog app"""
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
                # ========= event logging ==============
                event = UserLogs()
                event.save_log(current_user.id,send_comment.__doc__,comment)
                # ========= end of event logging========
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
    """user send reply for any comment in blog app"""
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
            # ========= event logging ==============
            event = UserLogs()
            event.save_log(current_user.id,send_reply.__doc__,reply)
            # ========= end of event logging========
            flash(f'your comment for comment {comment.title} is saved', 'success')
        except IntegrityError as ie:
            db.session.rollback()
            flash(f'error {ie} is happened, please try again', 'danger')
        except Exception as e:
            flash(f'error {e} is happened !!, please try again', 'danger')
        finally:
            return redirect(request.referrer)
    return redirect(request.referrer)
           

@blog.route('comments-list')
def comments_list():
    """list all comment for admin"""
    page = request.args.get('page', default=1, type=int)
    all_comments = Comment.query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=7)
    
    for comment in all_comments:
        comment.created_at = JalaliDateTime.to_jalali(comment.created_at)
    
    
    return render_template('blog/comments-list.html', all_comments=all_comments) 


@blog.route('comments-not-confirm')
def comments_not_confirm():
    """show not confirm comments"""
    page = request.args.get('page', default=1, type=int)
    comments_not_confirm = Comment.query.filter_by(show=False).paginate(page=page, per_page=7)
    print('comments_not_confirm', comments_not_confirm)
    for comment in comments_not_confirm:
        comment.created_at = JalaliDateTime.to_jalali(comment.created_at)
    
    
    return render_template('blog/comments-not-confirm.html', all_comments=comments_not_confirm) 
    

@blog.route('comment-in-news/<int:news_id>')
def comments_in_news(news_id):
    """show all comment for any news in blog app"""
    news = News.query.get_or_404(news_id)
    page = request.args.get('page', default=1, type=int)
    all_comments = Comment.query.filter_by(news_id=news_id).order_by(Comment.created_at.desc()).paginate(page=page, per_page=7)
    
    for comment in all_comments:
        comment.created_at = JalaliDateTime.to_jalali(comment.created_at)
    
    print('all comments is', all_comments.items)
    return render_template('blog/comments-list.html', all_comments=all_comments, news=news) 


@blog.route('comment-show/<int:comment_id>')
def comment_show(comment_id):
    """admin user can show or hidden a comment """
    comment = Comment.query.get_or_404(comment_id)
    if comment.show:
        comment.show = False
        flash(f'since time the reply {comment.title} is hidden', 'warning')
    else:
        comment.show = True
        flash(f'since time the reply {comment.title} is shown', 'success')
    db.session.add(comment)
    db.session.commit()
    # ========= event logging ==============
    event = UserLogs()
    event.save_log(current_user.id,comment_show.__doc__,comment)
    # ========= end of event logging========
    
    return redirect(request.referrer)


@blog.route('replies-list/<int:comment_id>')
def replies_list(comment_id):
    """show all replies of any comment in blog app"""
    comment = Comment.query.get_or_404(comment_id)
    page = request.args.get('page', default=1, type=int)
    all_replies = Reply.query.filter_by(comment_id=comment_id).order_by(Reply.created_at.desc()).paginate(page=page, per_page=7)
    
    for reply in all_replies:
        reply.created_at = JalaliDateTime.to_jalali(reply.created_at)
        
    return render_template('blog/replies-list.html', all_replies=all_replies, comment=comment, comment_id=comment_id)


@blog.route('reply-show/<int:reply_id>')
def reply_show(reply_id):
    """show or hidden replies by admin user"""
    reply = Reply.query.get_or_404(reply_id)
    if reply.show:
        reply.show = False
        flash(f'since time the reply {reply.title} is hidden', 'warning')
    else:
        reply.show = True
        flash(f'since time the reply {reply.title} is shown', 'success')
    db.session.add(reply)
    db.session.commit()
    # ========= event logging ==============
    event = UserLogs()
    event.save_log(current_user.id,reply_show.__doc__,reply)
    # ========= end of event logging========
    
    return redirect(request.referrer)
# ===================================== End Of Comment Function ====================================

# ================================== Category Function ==============================================
@blog.route('category-add', methods=['POST', 'GET'])
def category_add():
    """add category for news in blog app"""
    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category()
        category.title = request.form.get('title')
        try:
            db.session.add(category)
            db.session.commit()
            # ========= event logging ==============
            event = UserLogs()
            event.save_log(current_user.id,category_add.__doc__,category)
            # ========= end of event logging========
            flash('your category is added successfully', 'success')
        except IntegrityError:
            flash('the name is saved previously, please try by another name', 'warning')
        except Exception as ex:
            flash(f'error {ex} is happened, please try again', 'danger')
        finally:
            return redirect(url_for('blog.category_add', form=form))
    
    categories = Category.query.all()
    
    return render_template('blog/category-add.html', form=form, categories=categories)


@blog.route('category-edit/<string:cat_title>', methods=['POST', 'GET'])
def category_edit(cat_title):
    """edit category of news in blog app"""
    form = CommentForm()
    category = Category.query.filter_by(title=cat_title).one()
    if request.method == 'POST' and form.validate_on_submit():
        category.title = request.form.get('title')
        try:
            db.session.add(category)
            db.session.commit()
            # ========= event logging ==============
            event = UserLogs()
            event.save_log(current_user.id,category_edit.__doc__,category)
            # ========= end of event logging========
            flash('your category is editted successfully', 'success')
        except IntegrityError:
            flash('the name is saved previously, please try by another name', 'warning')
        except Exception as ex:
            flash(f'error {ex} is happened, please try again', 'danger')
        finally:
            return redirect(url_for('blog.category_add', form=form))
    
    categories = Category.query.all()
    
    return render_template('blog/category-edit.html', form=form, category=category, categories=categories)


@blog.route('category-delete/<string:cat_title>', methods=['GET','POST'])
def category_delete(cat_title):
    """delete a category from blog app"""
    form = CommentForm()
    category = Category.query.filter_by(title=cat_title).one()
    db.session.delete(category)
    db.session.commit()
    # ========= event logging ==============
    event = UserLogs()
    event.save_log(current_user.id,category_delete.__doc__,category)
    # ========= end of event logging========
    
    categories = Category.query.all()
    return redirect(url_for('blog.category_add', form=form, categories=categories))


@blog.route('category-news/<string:cat_title>')
def category_news(cat_title):
    """show news by category filter in blog app"""
    category = Category.query.filter_by(title=cat_title).first()
    news_all = category.news_all

    return render_template('blog/category-news.html', news_all=news_all)
# End Of Category Function