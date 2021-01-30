import copy
import os
import random
import string
import yaml

from flask import abort, Flask, redirect, render_template, request, url_for
from markupsafe import escape


CONFIG_FILE = os.environ.get("CONFIG") or "codes.yaml"


def create_app():
    app = Flask(__name__)

    with open(CONFIG_FILE, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    stages = add_prefixes(config["stages"])
    taunts = config["taunts"]

    @app.route("/")
    def start():
        first_stage = url_for("stage", prefix=stages[0]["prefix"], number=1)
        return render_template("start.html", first_stage=first_stage)

    @app.route("/<prefix>/<int:number>", methods=["GET", "POST"])
    def stage(prefix, number):
        stage_number = int(escape(number))
        stage = stages[number - 1]
        stage["number"] = stage_number

        if not stage or prefix != stage["prefix"]:
            abort(404)

        taunt = False

        if request.method == "POST":
            solution = stage["code"]

            guess = ""
            for i in range(3):
                guess += escape(request.form[f"digit{i}"])

            if int(guess) == solution:
                return redirect_to_stage_after(stage_number)

            taunt = True

        return render_template("stage.html", stage=stage, taunt=taunt, taunts=taunts)

    end_prefix = config["end"]["prefix"] or generate_prefix()
    @app.route(f"/{end_prefix}/end")
    def end():
        return render_template("end.html")

    def redirect_to_stage_after(current_stage_number):
        next_number = current_stage_number + 1
        if next_number > len(stages):
            return redirect(url_for("end"))

        next_stage = stages[next_number - 1]
        return redirect(url_for("stage", prefix=next_stage["prefix"], number=next_number))

    # Print out all stage URLs when creating app
    with app.test_request_context():
        start_url = url_for("start")
        print(f"Start\t{start_url}")

        for i, stage in enumerate(stages, start=1):
            url = url_for("stage", prefix=stage["prefix"], number=i)
            print(f"Stage {i}\t{url}")

        end_url = url_for("end")
        print(f"End\t{end_url}")

    return app


def add_prefixes(stages):
    prefixed_stages = copy.deepcopy(stages)
    for i, _ in enumerate(prefixed_stages):
        if not prefixed_stages[i]["prefix"]:
            prefixed_stages[i]["prefix"] = generate_prefix()
    return prefixed_stages


def generate_prefix(size=6, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
