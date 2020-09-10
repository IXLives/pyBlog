import os
from flask import Flask

# App Factory


def create_app(test_config=None):
    # Create a flask instance -- module name, yes files are relative
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='nine',
        DATABASE=os.path.join(app.instance_path, 'pyblog.sqlite'),
    )

    # Check for test env
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Obligatory Greeting
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    return app
