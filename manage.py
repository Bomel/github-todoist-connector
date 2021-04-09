import json
from flask import Flask
from sync_tasks import main

app = Flask(__name__)


@app.route('/')
def index():
    main()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    from waitress import serve
    print("Server is listening to http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)
