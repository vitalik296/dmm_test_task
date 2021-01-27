from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_login import LoginManager

from lib.Gamer.Gamer import Gamer
from lib.Gamer.GamerResource import GamerResource
from view.auth import auth
from view.view import view

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-puper-secret-key'

CORS(app)
login_manager = LoginManager()
login_manager.init_app(app=app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    return Gamer().get_by_id(user_id)


app.register_blueprint(view)
app.register_blueprint(auth)
api.add_resource(GamerResource, "/api/gamer/<gamer>", "/api/gamer")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
