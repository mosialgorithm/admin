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




class Development(Config):
    DEBUG = True




class Production(Config):
    DEBUG = False
    