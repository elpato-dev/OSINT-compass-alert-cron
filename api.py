from flask import Flask, request
import asyncio
import os
from dotenv import load_dotenv
from functools import wraps
from flask import Flask, request, jsonify

from alerter import send_alerts

# API Key functionality
load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("OSINT_COMPASS_API_KEY")

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('apikey') != API_KEY:
            return jsonify({'error': 'Invalid API key.'}), 403
        return view_function(*args, **kwargs)
    return decorated_function


@app.route('/alert', methods=['GET'])
@require_api_key
def alert():
    asyncio.run(send_alerts())
    return 'Alerts sent', 200

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#remove before deploying on render
#if __name__ == '__main__':
#    app.run()