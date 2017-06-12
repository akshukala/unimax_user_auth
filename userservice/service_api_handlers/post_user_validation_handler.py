from flask import session
from django.contrib.auth.models import User


def handle_request(username, password, remember_me):
    """
      This method is used to handle the request
      of authorizing a user.
    """

    authorized = False

    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            authorized = True
            session['user_id'] = user.id
            session['password_hash'] = user.password

            if remember_me:
                session.permanent = True

    except User.DoesNotExist:
        authorized = False

    return authorized


if __name__ == "__main__":
    print handle_request('akshay@nimbrisk.com', 'a', True)

