
from flask import render_template, flash, redirect, url_for, request 
from app import app, query
import sqlite3
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template
from app import login
from app.models import User, Cat
from app.forms import AddKittenForm, DeleteLitterForm, LoginForm, AddCatForm, UpdateCatForm, UpdateLitterForm, AddLitterForm, DeleteCatForm, DeleteLitterForm, AddKittenForm, RemoveKittenForm
import os
import datetime
import json

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
    available_kittens = query.get_available_kittens()
    return render_template('meet-our-cats/available-kittens.html', available_kittens=available_kittens)

@app.route('/expecting-litters')
def expecting_litters():
    litters = query.get_expecting_litters()
    return render_template('meet-our-cats/expecting-litters.html', litters=litters)

@app.route('/our-breeders')
def our_breeders():
    cats = query.get_breeding_cats()
    return render_template('meet-our-cats/our-breeders.html', cats = cats)

@app.route('/sold-kittens')
def sold_kittens():
    sold_cats = query.get_sold_cats()
    return render_template('meet-our-cats/sold-kittens.html', cats = sold_cats)

@login.user_loader
def load_user(user_id):
    '''Finds the data for the user id and returns a User object with that data'''
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    user_data = cur.execute("SELECT * FROM users WHERE username = (?)", (user_id,)).fetchone()
    connection.commit()
    user = User(user_data[0], user_data[1])
    return user

@app.route('/catqueries', methods=['GET', 'POST'])
def handle():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    form_data = request.form
    print("DATA TO HANDLE" + str(form_data))

    #find out what kind of form submitted to us by looking at the submit button
    submission_type = form_data.get('submit')
    print('SUBMISSION TYPE')
    print(submission_type)

    #depending on the submission type, do something 
    #CREATE A NEW CAT
    if submission_type == 'Create Cat':
        #get all the data in the form
        name = form_data.get('name', None)
        description = form_data.get('description', None)
        sex = form_data.get('sex', None)
        forsale = form_data.get('forsale', None)
        sold = form_data.get('sold', None)
        color = form_data.get('color', None)
        breeder = form_data.get('breeder', None)
        birthdate = form_data.get('birthdate', None)

        #set up image path
        image = form_data.get('photo.data', None)
        if image:
            image_path = os.path.join(app.config['UPLOAD_PATH'], image.filename)
            image.save("app/" + image_path)
        else:
            image_path = None

        cat = Cat(name, birthdate, color, sex, description, image, forsale, breeder, sold)
        query.create_cat(cat)
    #UPDATE AN EXISTING CAT
    elif submission_type == 'Update Cat':
        #get all the data in the form
        name = form_data.get('name', None)
        description = form_data.get('description', None)
        sex = form_data.get('sex', None)
        forsale = form_data.get('forsale', 0)
        sold = form_data.get('sold', 0)
        color = form_data.get('color', None)
        breeder = form_data.get('breeder', 0)
        birthdate = form_data.get('birthdate', None)

        #set up image path
        image = form_data.get('photo.data', None)
        if image:
            image_path = os.path.join(app.config['UPLOAD_PATH'], image.filename)
            image.save("app/" + image_path)
        else:
            image_path = None

        cat = Cat(name, birthdate, color, sex, description, image, forsale, breeder, sold)
        query.update_cat(cat)
    #DELETE A CAT
    elif submission_type == 'Delete Cat?':
        print('DELETE CAT')
        name = form_data.get('name', None)
        query.delete_cat(name)
    #CREATE A NEW LITTER
    elif submission_type == 'Create Litter':
        print("CREATE LITTER")
        father = form_data.get('father', None)
        mother = form_data.get('mother', None)
        duedate = form_data.get('duedate', None)
        birthdate = form_data.get('birthdate', None)
        query.create_litter(mother, father, birthdate, duedate)
    #UPDATE AN EXISTING LITTER
    elif submission_type == 'Update Litter':
        print("UPDATE LITTER")
        father = form_data.get('father', None)
        mother = form_data.get('mother', None)
        duedate = form_data.get('duedate', None)
        birthdate = form_data.get('birthdate', None)
        born = form_data.get('born')
        public = form_data.get('public')
        query.update_litter(mother, father, birthdate, duedate,born, public)
    #DELETE A LITTER
    elif submission_type == 'Delete litter?':
        print("DELETE LITTER")
        father = form_data.get('father', None)
        mother = form_data.get('mother', None)
        duedate = form_data.get('duedate', None)
        query.delete_litter(mother, father, duedate)
    #ADD A KITTEN TO A LITTER
    elif submission_type == 'Add kitten':
        litter_data = form_data.get('litter').split("|")
        print(litter_data)
        mother = litter_data[0]
        father = litter_data[1]
        duedate = litter_data[2]
        kitten = form_data.get('kitten')
        query.add_kitten_to_litter(mother, father, kitten, duedate)
    #REMOVE KITTEN FROM LITTER
    elif submission_type == 'Remove kitten':
        litter_data = form_data.get('litter').split("|")
        mother = litter_data[0]
        father = litter_data[1]
        kitten = form_data.get('kitten')
        print(mother, father, kitten)
        query.remove_kitten_from_litter(mother, father, kitten)
    return redirect(url_for('admin'))

@login_required
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    #if we are logged in, show the admin dashboard
    if current_user.is_authenticated:
        #define forms
        createcatform = AddCatForm()
        updatecatform = UpdateCatForm()
        deletecatform = DeleteCatForm()

        createlitterform = AddLitterForm()
        updatelitterform = UpdateLitterForm()
        deletelitterform = DeleteLitterForm()

        addkittenform = AddKittenForm()
        removekittenform = RemoveKittenForm()

        #get the button that made the request for this page, if any
        form_data = request.form
        print("THE FORM TAHT MADE ADMIN"+ str(form_data))
        form = None
        if request.form.get('addcat'):
            form = "createcat"
        if request.form.get('updatecat'):
            catname = request.form.get('updatecat')
            cat = query.get_cat_by_name(catname)
            updatecatform = UpdateCatForm(obj=cat)
            print("CAT DETAILS")
            print(cat.forsale, cat.breeding, cat.sold)
            if cat.forsale == 1:
                updatecatform.forsale.data = True
            if cat.breeding == 1:
                updatecatform.breeder.data = True
            if cat.sold == 1:
                updatecatform.sold.data = True
            form = "updatecat"
        if request.form.get('addlitter'):
            form = "createlitter"
        if request.form.get('updatelitter'):
            litter = request.form.get('updatelitter').split("|")
            print('LITTER' + str(litter))
            father = litter[0]
            mother = litter[1]
            duedate = litter[2]
            birthdate = litter[3]
            public = litter[4]
            born = litter[5]
            print("BORN AND PUBLIC")
            print(born, public)
            litter = query.get_litter(mother, father, duedate, birthdate)
            updatelitterform = UpdateLitterForm(obj=litter)
            if public=="1":
                updatelitterform.public.data = True
            if born=="1":
                updatelitterform.born.data = True
            form='updatelitter'
        if request.form.get('deletecat'):
            catname = request.form.get('deletecat')
            deletecatform = DeleteCatForm(data={'name': catname})
            form='deletecat'
        if request.form.get('deletelitter'):
            litter = request.form.get('deletelitter').split("|")
            father = litter[0]
            mother = litter[1]
            duedate = datetime.datetime.strptime(litter[2], "%Y-%m-%d")
            deletelitterform = DeleteLitterForm(data={'father': father, 'mother':mother, 'duedate':duedate})
            form='deletelitter'
        if request.form.get('addkitten'):
            form = 'addkitten'
        if request.form.get('removekitten'):
            form = 'removekitten'
        
        #get current  cat and litter data 
        litters = query.get_litters()
        print("LITTERS" + str(litters))
        for litter in litters:
            print(litter.born, litter.public)
        cats = query.get_cats()

        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        #get names of cats that could be kitten parents - this is for the right side which does not change
        mothers = cur.execute("SELECT catname FROM cats WHERE sex='female' AND breeding=1").fetchall()
        fathers = cur.execute("SELECT catname FROM cats WHERE sex ='male' AND breeding=1").fetchall()
        catnames = cur.execute("SELECT catname FROM cats").fetchall()
        createcatform.mother.choices += [(mother[0], mother[0]) for mother in mothers]
        createcatform.father.choices += [(father[0], father[0]) for father in fathers]

        updatecatform.mother.choices += [(mother[0], mother[0]) for mother in mothers]
        updatecatform.father.choices += [(father[0], father[0]) for father in fathers]

        createlitterform.mother.choices += [(mother[0], mother[0]) for mother in mothers]
        createlitterform.father.choices += [(father[0], father[0]) for father in fathers]

        updatelitterform.mother.choices += [(mother[0], mother[0]) for mother in mothers]
        updatelitterform.father.choices += [(father[0], father[0]) for father in fathers]

        deletelitterform.mother.choices += [(mother[0], mother[0]) for mother in mothers]
        deletelitterform.father.choices += [(father[0], father[0]) for father in fathers]

        addkittenform.kitten.choices += [(cat[0], cat[0]) for cat in catnames]
        removekittenform.kitten.choices += [(cat[0], cat[0]) for cat in catnames]
        litternames =  [(str(litter.mother)+ "|" +str(litter.father)+ "|" +str(litter.birthdate) , str(litter)) for litter in litters]
        addkittenform.litter.choices += litternames
        removekittenform.litter.choices += litternames


        return render_template('admin.html', createcatform = createcatform, updatecatform=updatecatform, deletecatform=deletecatform, createlitterform=createlitterform, updatelitterform=updatelitterform, deletelitterform=deletelitterform, addkittenform=addkittenform, removekittenform=removekittenform, cats = cats, litters=litters, form=form)
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
