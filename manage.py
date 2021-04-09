import json
from flask import Flask
from sync_tasks import main

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    main()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
