import requests
from functools import wraps

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if 'api_key' in request.args and str(request.args['api_key']) == str(API_KEY):
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
