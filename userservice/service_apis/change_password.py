from flask import Flask, request, session
from flask import current_app as app
from userservice.utils.auth import get_user
from userservice.utils.resource import Resource

class ChangePassword(Resource):
    def post(self):
        app.logger.debug("Received change password request for %s", str(get_user().id))
        print request.__dict__
        current_password = str(request.json['currentPassword'])
        new_password = str(request.json['newPassword'])
        u = get_user()
        if not u.check_password(current_password):
            return {"errorCode": 422,
                    "errorMessage": "Wrong Current Password"}
        u.set_password(new_password)
        u.save()
        return {"message": "Password Changed succesfully"}
