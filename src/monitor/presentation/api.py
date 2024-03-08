from flask import Blueprint

bp: Blueprint = Blueprint("monitor",__name__)
bp_prefix: str = "/monitor"

@bp.route("/", methods=["GET"])
def get():
    return "Monitor is running"
