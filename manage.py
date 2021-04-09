import json
from flask import Flask
from sync_tasks import main

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    global in_use
    if in_use:
        print("Process in use!")
        return json.dumps({'success': True, 'in_use': True}), 200, {'ContentType': 'application/json'}
    else:
        in_use = True
        main()
        in_use = False
        return json.dumps({'success': True, 'in_use': False}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    global in_use
    in_use = False
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
