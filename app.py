from flask import abort, Flask, url_for
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

    @app.route('/<prefix>/<int:code_number>')
    def show_code(prefix, code_number):
        number = int(escape(code_number))
        code = config["codes"].get(number)

        if not code or prefix != code["prefix"]:
            abort(404)

        solution = code["code"]
        return f'Code {number} is {solution}'

    with app.test_request_context():
        for code_number in config["codes"]:
            prefix = config["codes"][code_number]["prefix"]
            url = url_for('show_code', code_number=code_number, prefix=prefix)
            print(f"Code {code_number}\t{url}")

    return app