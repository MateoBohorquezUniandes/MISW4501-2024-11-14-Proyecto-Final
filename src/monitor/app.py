from flask import Flask, jsonify


def create_app():
    
    app = Flask(__name__, instance_relative_config=True)

    from .presentation.api import bp, bp_prefix
    app.register_blueprint(bp, url_prefix=bp_prefix)

    from .application.scheduler import start_job
    #start the scheduler
    start_job()
    return app
