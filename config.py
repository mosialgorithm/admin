import os 



class Config(object):
    # ========================================================================================
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456789@localhost/dashboard"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    # SQLALCHEMY_TRACK_MODIFICATIONS = "False"
    # ========================================================================================
    UPLOAD_DIR = os.path.curdir + '/static/uploads/'
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SECRET_KEY = "my_name_is_mostafa_ghorbani"
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB')
    # ===================================================================================
    CKEDITOR_PKG_TYPE = os.getenv('CKEDITOR_PKG_TYPE')
    CKEDITOR_SERVE_LOCAL = os.getenv('CKEDITOR_SERVE_LOCAL')
    CKEDITOR_LANGUAGE = os.getenv('CKEDITOR_LANGUAGE')
    CKEDITOR_CODE_THEME = os.getenv('CKEDITOR_CODE_THEME')
    CKEDITOR_PKG_TYPE = os.getenv('CKEDITOR_PKG_TYPE')
    CKEDITOR_ENABLE_CSRF = os.getenv('CKEDITOR_ENABLE_CSRF')
    CKEDITOR_SERVE_LOCAL = os.getenv('CKEDITOR_SERVE_LOCAL')
    




class Development(Config):
    DEBUG = True




class Production(Config):
    DEBUG = False
    