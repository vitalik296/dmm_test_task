from flask import Blueprint, request, flash, url_for, render_template
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from lib.Gamer.Gamer import Gamer

auth = Blueprint("auth", __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template("signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    gamer_login = request.form.get('login')
    password = request.form.get('password')

    user = Gamer().get_by_login(gamer_login)

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    Gamer().create_gamer({"name": name,
                          "login": gamer_login,
                          "password": generate_password_hash(password, method='sha256')})

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    gamer_login = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Gamer().get_by_login(gamer_login)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('view.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.index'))
