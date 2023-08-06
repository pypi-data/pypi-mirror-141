from pathlib import Path
import pkg_resources
from shutil import copy

import click
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from archivy_espial import config
from archivy import app
from espial import create_app


@click.command(
    help=f"Run Archivy with Espial"
)
def espial():
    with app.app_context():
        user_dir = Path(app.config["USER_DIR"])
        # load JS extension
        if not app.config.get("DATAOBJ_JS_EXTENSION", False):
            if not (user_dir / "espial.js").exists():
                js_file = Path(pkg_resources.resource_filename('archivy_espial', 'espial.js'))
                copy(js_file, user_dir)
            app.config["DATAOBJ_JS_EXTENSION"] = "espial.js"
        esp_config = user_dir / "espial.py"
        try:
            # load ESPIAL config
            contents = open(esp_config)
            config_locals = {}
            exec(contents.read(), globals(), config_locals)
            contents.close()
            esp_config = config_locals.get("Config", config.Config)()
        except FileNotFoundError:
            esp_config = config.Config()
        esp_config.data_dir = user_dir / "data"
        merged_app = DispatcherMiddleware(app, {
            '/espial': create_app(esp_config)
        })
        # run app
        run_simple(app.config["HOST"], app.config["PORT"], merged_app)
