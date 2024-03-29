import logging
from logging.handlers import RotatingFileHandler

from flask import Flask




from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from redis import StrictRedis

from config import config
from info.utils.common import do_index_class

db = SQLAlchemy()

redis_store = None  # type: StrictRedis



def setup_log(config_name):

    logging.basicConfig(level=config[config_name].LOG_LEVEL)

    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)

    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

    file_log_handler.setFormatter(formatter)

    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    setup_log(config_name)

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)

    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT,decode_responses=True)


    CSRFProtect(app)

    Session(app)

    app.add_template_filter(do_index_class,"index_class")

    @app.after_request
    def after_request(response):
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token",csrf_token)
        return response


    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    return app
