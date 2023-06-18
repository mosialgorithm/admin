from flask import Blueprint


clinic = Blueprint('clinic', __name__, url_prefix='/clinic/')



from . import views