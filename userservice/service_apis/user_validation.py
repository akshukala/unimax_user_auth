#from agroutils.exceptions.error_handler import ErrorHandler

from flask import Flask, request, session
from flask import current_app as app
from flask.ext import restful

from userservice.conf.config_logger_setup import setup_config_logger
from userservice.service_api_handlers import \
    post_user_validation_handler, delete_user_validation_handler
from userservice.utils.resource import Resource
from userservice.utils.auth import get_user
#from userservice.utils.utility_funcs import send_exception_mail


class UserValidation(Resource):

 #   @ErrorHandler("Post User Validation", app, send_exception_mail)
    def post(self):
        """
           This method is used to authorize the
           user
        """
        app.logger.debug("Received login request for %s",
                         request.json['emailId'])
        is_authorized = post_user_validation_handler.handle_request(
            request.json['emailId'],
            request.json['password'],
            request.json['rememberMe']
        )

        if is_authorized:
            app.logger.info("Validated the login credentials for %s",
                            request.json['emailId'])
            return {
                'responseData': {
                    'name': get_user().get_full_name(),
                    app.auth_header_name: session.get('key'),
                    'is_authorized': is_authorized,
                }
            }
        else:
            app.logger.exception("Invalid username or password %s",
                                 request.remote_addr)
            return {
                'errorMessage':
                    'The email or password you entered is incorrect',
                'errorCode': 403
            }

    # This method is exempted from authentication
    post.authenticated = False

   # @ErrorHandler("Delete User Validation", app, send_exception_mail)
    def delete(self):
        """
        Delete the authentication session.
        """
        try:
            logged_in_user = get_user()
            app.logger.info("Logout called for the user %s",
                            logged_in_user.email)
        except NotAuthenticatedException:
            app.logger.info("Logout called for an invalid session %s",
                            request.remote_addr)

        delete_user_validation_handler.handle_request(request)
        return {
            'responseData': {
                'is_deleted': True
            }
        }
    delete.authenticated = False

if __name__ == '__main__':
    test_app = Flask(__name__)
    test_api = restful.Api(test_app)
    setup_config_logger(test_app)
    test_api.add_resource(RecruiterValidation, '/uservalidation/')
    test_app.run()
