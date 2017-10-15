from flask import Flask, jsonify, request, redirect, current_app
import requests
from functools import wraps

application = Flask(__name__)


GOOG_API=open('apikey.txt', 'r').readline()

def support_jsonp(f):
    """Wraps output to JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = jsonify(f(*args, **kwargs))
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(result.data) + ')'
            return current_app.response_class(content,
                                              mimetype='application/json')
        else:
            return result
    return decorated_function

@application.route("/")
@support_jsonp
def home():
    url = None
    args = {key: value for key, value in request.args.iteritems() if key != 'callback' and not key.startswith('_')}
    base = request.args.get('_base', 'http://waxmansgym.com/calculator')
    argstring = '&'.join(['{}={}'.format(key, value) for key, value in args.iteritems()])
    url = '{}/?{}'.format(base, argstring)
    data = {'longUrl': url}
    r = requests.post('https://www.googleapis.com/urlshortener/v1/url?key={}'.format(GOOG_API), json=data)
    result = r.json()
    return {'url': result['id']}

if __name__ == "__main__":
    application.run(host='0.0.0.0')
