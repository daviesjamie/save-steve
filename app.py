from flask import Flask, url_for
from markupsafe import escape
import os
import yaml

CONFIG_FILE = os.environ.get("CONFIG") or "codes.yaml"


def create_app():
    app = Flask(__name__)

    with open(CONFIG_FILE, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    @app.route('/code/<int:code_number>')
    def show_code(code_number):
        number = int(escape(code_number))
        code = config["codes"][number]["code"]
        return f'Code {number} is {code}'

    with app.test_request_context():
        for code in config["codes"]:
            url = url_for('show_code', code_number=code)
            print(f"Code {code}\t{url}")

    return app