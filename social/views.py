from persiantools.jdatetime import JalaliDateTime, digits
from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import social
from .models import Post, PostLike, PostComment, CommentLike, Following
from .forms import NewPostForm, PostCommentForm, FollowingForm
from flask_login import login_user, logout_user, current_user
from utils import save_avatar, jdt_from_pdp, jdt_to_gregorian
from sqlalchemy.exc import IntegrityError
from auth.models import User, UserLogs
from admin.forms import UserEditForm




@social.route('/<string:username>')
def index(username):
    """welcome to social networking"""
    post_form = NewPostForm()
    user_form = UserEditForm()
    comment_form = PostCommentForm()
    follow_form = FollowingForm()
    user = User.query.filter_by(username=username).first()
    following = Following.query.filter_by(follow_from=user.id).all()
    followed = Following.query.filter_by(follow_to=user.id).all()
    user_following = [user.follow_to for user in following]
    user_followed = [user.follow_from for user in followed]
    # ==========================================
    posts = Post.query.order_by(Post.created_at.desc()).all()
    all_posts = []
    for post in posts:
        if post.user_id in user_following or post.user_id == user.id:
            all_posts.append(post)
    # ==========================================
    user_form.about_me.data = user.about_me
    
    return render_template('social/index.html',
                           user_form=user_form, post_form=post_form, comment_form=comment_form, follow_form=follow_form,
                           all_posts=all_posts, user=user, user_following=user_following, user_followed=user_followed)


@social.route('/user-info-update', methods=['POST'])
def user_info_update():
    post_form = NewPostForm()
    user_form = UserEditForm()
    if user_form.validate_on_submit():
        current_user.education = f"{request.form.get('education_degree')}###{request.form.get('education_field')}###{request.form.get('education_area')}"
        current_user.skills = f"{request.form.get('skill_one')}###{request.form.get('skill_two')}###{request.form.get('skill_three')}###{request.form.get('skill_four')}###{request.form.get('skill_five')}"
        current_user.address = f"{request.form.get('address_province')}###{request.form.get('address_city')}###{request.form.get('address_street')}"
        current_user.about_me = f"{request.form.get('about_me')}"
        
        try:
            db.session.add(current_user)
            db.session.commit()
            flash('your data is saved', 'success')
        except:
            db.session.rollback()
            flash('your data is not correctly', 'warning')
        finally:
            return redirect(url_for('social.index', username=current_user.username, user_form=user_form, post_form=post_form))


@social.route('post-create/<int:user_id>', methods=['POST'])
def post_create(user_id):
    if request.method == 'POST':
        post = Post()
        post.content = request.form.get('post')
        post.user_id = user_id
        db.session.add(post)
        db.session.commit()
        flash('your post is sent successfully', 'success')
        return redirect(request.referrer)


@social.route('post-like/<int:post_id>/<int:user_id>')
def post_like(post_id, user_id):
    old_liked = PostLike.query.filter_by(post_id=post_id, user_id=user_id).first()
    if old_liked:
        db.session.delete(old_liked)
        db.session.commit()
        return redirect(request.referrer)
    post_like = PostLike()
    post_like.user_id = user_id
    post_like.post_id = post_id
    try:
        db.session.add(post_like)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    finally:
        return redirect(request.referrer)
    
    
@social.route('post-comment/<int:post_id>/<int:user_id>', methods=['POST'])
def post_comment(post_id, user_id):
    form = PostCommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = request.form.get('comment')
            post_comment = PostComment()
            post_comment.comment = comment
            post_comment.post_id = post_id
            post_comment.user_id = user_id
            try:
                db.session.add(post_comment)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            finally:
                return redirect(request.referrer)
                      
            
@social.route('comment-like/<int:comment_id>/<int:user_id>')
def comment_like(comment_id, user_id):
    old_like = CommentLike.query.filter_by(comment_id=comment_id, user_id=user_id).first()
    if old_like:
        db.session.delete(old_like)
        db.session.commit()
        return redirect(request.referrer)
    comment_like = CommentLike()
    comment_like.user_id = user_id
    comment_like.comment_id = comment_id
    try:
        db.session.add(comment_like)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    finally:
        return redirect(request.referrer)
        

@social.route('search-user')
def search_user():
    users = User.query.all()
    follow_form = FollowingForm()
    following = Following.query.filter_by(follow_from=current_user.id).all()
    print('following : ', following)
    me_following = [user.follow_to for user in following]
    print('me folloeing : ', me_following)
    return render_template('social/search-user.html', users=users, me_following=me_following, follow_form=follow_form)


@social.route('following/<int:user_id>', methods=['POST'])
def following(user_id):
    if current_user.id == user_id:
        return redirect(request.referrer)
    
    follow_form = FollowingForm()
    if follow_form.validate_on_submit():
        following = Following()
        old_following = Following.query.filter_by(follow_from=current_user.id, follow_to=user_id).first()
        if old_following:
            db.session.delete(old_following)
            db.session.commit()
            return redirect(request.referrer)
        
        following.follow_from = current_user.id 
        following.follow_to = user_id
        try:
            db.session.add(following)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            return redirect(request.referrer)
    