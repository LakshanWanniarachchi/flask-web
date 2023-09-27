
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        global user

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Log in Success', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", k=current_user.is_authenticated)


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        fname = request.form.get("fName")
        lname = request.form.get("lname")
        email = request.form.get("email")
        uname = request.form.get("uname")
        Password = request.form.get("Password")
        repassword = request.form.get("repassword")

        if len(fname) < 4:
            flash('Fist name must be grater than 4 chactors', category="error")

        elif len(lname) < 4:
            flash('Last name must be grater than 4 chactors', category="error")
        elif Password != repassword:
            flash('Paasword not match !', category="error")
        elif len(Password) < 7:
            flash('password must be grater than 7 chactors', category="error")
        else:
            new_user = User(email=email, fname=fname, lname=lname,
                            password=generate_password_hash(Password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Acount created !', category="success")

            return redirect(url_for('views.home'))

    return render_template("singup.html", k=current_user.is_authenticated)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
