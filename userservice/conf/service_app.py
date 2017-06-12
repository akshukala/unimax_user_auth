from os.path import dirname, abspath

import django
from django.db import close_old_connections
from flask import Flask
from flask.ext import restful
from uni_db.settings.pool import init_pool

from userservice.conf.config_logger_setup import setup_config_logger
from userservice.session.interfaces import DBInterface

from userservice.service_apis.user_validation import UserValidation

from userservice.service_apis.change_password import ChangePassword
#from userservice.service_apis.mobile_user import MobileUser

from flask.ext.cors import CORS

close_old_connections()
init_pool()

django.setup()
app = Flask(__name__)
CORS(app)
app.auth_header_name = 'X-Authorization-Token'
app.session_interface = DBInterface()
app.root_dir = dirname(dirname(abspath(__file__)))

api = restful.Api(app)

setup_config_logger(app)

app.logger.info("Setting up Resources")

api.add_resource(UserValidation, '/userservice/uservalidation/')
api.add_resource(ChangePassword, '/userservice/changepassword/')
#api.add_resource(MobileUser, '/userservice/mobileuser/')
app.logger.info("Resource setup done")

if __name__ == '__main__':
    # from gevent import monkey
    # from userservice.utils.hacks import gevent_django_db_hack
    # gevent_django_db_hack()
    # monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False, aggressive=True)
    app.run(host="0.0.0.0", port=7281)
