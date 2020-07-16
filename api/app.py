from flask import Flask

app = Flask(__name__)


@app.route('/planets', methods=['GET', 'POST'])
def planets():
    return {}
