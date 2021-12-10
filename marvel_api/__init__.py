from flask import Flask 
from config import Config
from .authentication.routes import auth
from .site.routes import site
from .api.routes import api 
from .models import db, User, login_manager
from flask_migrate import Migrate
from flask_cors import CORS 
from .helpers import JSONEncoder 
# marvel-env\Scripts\Activate
# set FLASK_APP=marvel-api
# set FLASK_ENV=development

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'
migrate = Migrate(app, db)
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
CORS(app)

app.json_encoder = JSONEncoder