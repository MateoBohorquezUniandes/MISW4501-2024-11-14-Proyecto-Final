import seedwork.presentation.api as api
from flask import Blueprint, Response, jsonify, request

bp_prefix: str = "/perfiles/queries"
bp: Blueprint = api.create_blueprint("queries", bp_prefix)
