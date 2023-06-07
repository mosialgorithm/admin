import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, flash, redirect, url_for
from config import Development
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from flask_moment import Moment
from flask_redis import Redis
from persiantools.jdatetime import JalaliDateTime
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect





base_dir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)

app.config.from_object(Development)




# ================= CONFIGS_OF_LOGIN_MANAGER ==========================
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'info'
login.init_app(app)
# ====================================================================

db = SQLAlchemy(app)

migrate = Migrate(app, db, compare_type=True)

moment = Moment(app)

redis = Redis(app)

ckeditor = CKEditor(app)

csrf = CSRFProtect(app)



# ================= SET_GLOBAL_VARIABLES ==========================
@app.context_processor
def user_list():
    # users = User.query.order_by(User.id.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()
    prime_users = []
    active_users = []
    for user in users:
        if user.active == 1:
            active_users.append(user)
        if user.role == 1:
            prime_users.append(user)
    return dict(all_users=users, userslist=users, prime_users=prime_users, active_users=active_users)
# ================= END_OF_SET_GLOBAL_VARIABLES ==========================
@app.context_processor
def blog_funcs():
    from blog.models import Comment, News
    comments_not_confirm = Comment.query.filter_by(show=False).all()
    all_news_draft = News.query.filter_by(draft=1).order_by(News.created_at.desc()).all()
    return dict(comments_not_confirm=comments_not_confirm,all_news_draft=all_news_draft)
    

# @app.context_processor
# def show_category():
#     from blog.models import Category
#     categories = Category.query.all()
#     return dict(categories=categories)




@login_required
@app.route('/')
def index():
    return redirect(url_for('admin.index'))



# ================= ADD_BLUEPRINTS =============================
from auth import auth
from admin import admin
from blog import blog
from social import social
from quiz import quiz


app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(blog)
app.register_blueprint(social)
app.register_blueprint(quiz)
# ==============================================================

# ================================ User Handler ==========================
from auth.models import User


@login.user_loader
def userLoader(user_id):
    return User.query.get(user_id)


@login.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.', 'danger')
    return redirect(url_for('auth.login'))

# ==========================================================================




@app.errorhandler(404)
def NotFound(error):
    return render_template('404.html', error=error)




# @app.before_request
# def before_request_func():
#     from blog.models import News
#     news = News.query.filter_by(draft=1).all()
#     from datetime import datetime
#     for ns in news:
#         if ns.published_at >= datetime.now():
#             ns.draft = 0
#             db.session.add(ns)
#             db.session.commit()


# ================================ SCHEDULERING METHODS ============================================
def app_scheduler():
    with app.app_context():
        from blog.models import News
        from datetime import datetime
        all_news = News.query.filter_by(draft=1).all()
        for news in all_news:
            if news.published_at < datetime.today():
                news.draft = 0
                print(f'news by title {news.title} dont be draft from now')
                db.session.add(news)
                db.session.commit()
                
        print(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        print('---------------- programmer : mosi ------------------------')

scheduler = BackgroundScheduler()
scheduler.add_job(func=app_scheduler, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
# ====================================================================================================



if __name__ == '__main__':
    app.run(debug=True)
    