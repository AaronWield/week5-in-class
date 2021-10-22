from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from flask_migrate import Migrate
from .models import db, login_manager, ma
from flask_cors import CORS

# instantiating a new flask app
app = Flask(__name__)
app.config.from_object(Config)

# registering Blueprints to use within the scope of whole app
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

# instantiating db within the scope of app
db.init_app(app)

# instantiating marshmallow within the scope of app
ma.init_app(app)

# instantiating login_manager within the scope of app
login_manager.init_app(app)

# specifies what page to load for protected routes when a user is not loggged in
login_manager.login_view = 'auth.signin' 

# giving Flask migrate access to app and DB models
migrate = Migrate(app, db)

CORS(app)