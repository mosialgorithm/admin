import os
from flask import Flask, render_template, flash, redirect, url_for
from config import Development
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from flask_moment import Moment
from flask_redis import Redis
from persiantools.jdatetime import JalaliDateTime



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
    return dict(all_users=users, prime_users=prime_users, active_users=active_users)
# ================= END_OF_SET_GLOBAL_VARIABLES ==========================



@login_required
@app.route('/')
def index():
    return redirect(url_for('admin.index'))



# ================= ADD_BLUEPRINTS =============================
from auth import auth
from admin import admin
from blog import blog


app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(blog)
# ================= END_OF_BLUEPRINTS ==========================






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


@app.before_request
def before_request_func():
    from blog.models import News
    news = News.query.filter_by(draft=1).all()
    from datetime import datetime
    for ns in news:
        if ns.published_at >= datetime.now():
            ns.draft = 0
            db.session.add(ns)
            db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
    