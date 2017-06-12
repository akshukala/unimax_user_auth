from flask import session


def handle_request(request):
    """
      This method is used to handle the request
      of authorizing a user.
    """
    session['user_id'] = None
