from flask import Blueprint, render_template
from flask_login import login_required, current_user

from lib.Gamer.Gamer import Gamer

view = Blueprint('view', __name__, url_prefix='/')

POCKEMON_LIST = ["bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
                 "squirtle", "wartortle", "blastoise", "caterpie", "metapod"]

@view.route("/")
def index():
    return render_template("index.html", gamers=Gamer().get_all_gamers())


@view.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user, pokemon_list=POCKEMON_LIST)
