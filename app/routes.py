from flask import render_template, flash, redirect, url_for, request 
from app import app
import sqlite3
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template
from app import login
from app.models import User
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Munchranch", user="silvia")

@app.route('/responsible-breeding')
def responsible_breeding():
    return render_template('responsible-breeding.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/application')
def application():
    return render_template('application.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/breeder-info')
def breeder_info():
    return render_template('adoption/breeder-info.html')

@app.route('/bringing-kitten-home')
def bringing_home():
    return render_template('adoption/bringing-kitten-home.html')

@app.route('/conditions-for-sale')
def conditions_for_sale():
    return render_template('adoption/conditions-for-sale.html')

@app.route('/health-contract')
def health_contract():
    return render_template('adoption/health-contract.html')

@app.route('/pricing-discounts')
def pricing_discounts():
    return render_template('adoption/pricing-discounts.html')

@app.route('/waitlist')
def waitlist():
    return render_template('adoption/waitlist.html')

@app.route('/diet')
def diet():
    return render_template('cat-care/diet.html')

@app.route('/general-care')
def general_care():
    return render_template('cat-care/general-care.html')

@app.route('/resources')
def resources():
    return render_template('cat-care/resources.html')

@app.route('/second-cats')
def second_cats():
    return render_template('cat-care/second-cat-intro.html')

@app.route('/available-kittens')
def available_kittens():
    return render_template('meet-our-cats/available-kittens.html')

@app.route('/expecting-litters')
def expecting_litters():
    return render_template('meet-our-cats/expecting-litters.html')

@app.route('/our-breeders')
def our_breeders():
    cats = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM cats'):
        cats.append(row)
    return render_template('meet-our-cats/our-breeders.html', cats = cats)

@app.route('/sold-kittens')
def sold_kittens():
    return render_template('meet-our-cats/sold-kittens.html')

@login.user_loader
def load_user(user_id):
    '''Finds the data for the user id and returns a User object with that data'''
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    user_data = cur.execute("SELECT * FROM users WHERE username = (?)", (user_id,)).fetchone()
    connection.commit()
    user = User(user_data[0], user_data[1])
    return user

@login_required
@app.route('/admin')
def admin():
    if current_user.is_authenticated:
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        user_data = cur.execute('SELECT * FROM users WHERE username = (?)', (username,)).fetchone()
        if user_data:
            user = User(user_data[0], user_data[1])
            user.set_password_hash(user_data[2])
            print(user.name, user.password_hash)
            if not user.check_password(password):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/signup')
def signup():
    return 'Signup'

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
