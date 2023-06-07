from flask import Blueprint


quiz = Blueprint('quiz', __name__, url_prefix='/quiz/')



from . import views