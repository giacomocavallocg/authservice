import os
from main.app import create_app

config_name = os.getenv('FLASK_ENV', 'Development')

if config_name == 'Production':
    app = create_app(config_name="prod")
else:
    app = create_app(config_name="dev")