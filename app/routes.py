from flask import render_template
from app import app
import sqlite3

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Silvia'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan B Anthony'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title="Munchranch", user=user, posts=posts)

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