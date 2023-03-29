"""Flask default params"""

SECRET_KEY = 'SECRET_KEY'
##################################################

"""Flask sqlalchemy params"""

SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI'
SQLALCHEMY_TRACK_MODIFICATIONS = 'SQLALCHEMY_TRACK_MODIFICATIONS'
SQLALCHEMY_ECHO = 'SQLALCHEMY_ECHO'
database = 'postgresql:///feedback_db'

##################################################

"""Flask testing params"""

DEBUG_TB_INTERCEPT_REDIRECT = 'DEBUG_TB_INTERCEPT_REDIRECT'
TESTING = 'TESTING'
DEBUG_TB_HOSTS = 'DEBUG_TB_HOSTS'
dont_show_debug_toolbar = ['dont-show-debug-toolbar']

##################################################

"""Flask Mail"""

MAIL_SERVER = 'MAIL_SERVER'
MAIL_PORT = 'MAIL_PORT'
MAIL_USERNAME = 'MAIL_USERNAME'
MAIL_PASSWORD = 'MAIL_PASSWORD'
MAIL_USE_TLS = 'MAIL_USE_TLS'
MAIL_USE_SSL = 'MAIL_USE_SSL'
mail_smtp = 'smtp.gmail.com'
mail_port = 465

##################################################