from app import app
from app.models import Cat
import sqlite3
import datetime

#getters
def get_cat_by_id(id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cat = cat_from_row(cur.execute('SELECT * FROM cats WHERE id=?', (id,)).fetchone())
    return cat

def get_cat_by_name(name):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cat = cat_from_row(cur.execute('SELECT * FROM cats WHERE catname=?', (name,)).fetchone())
    return cat

def get_cats():
    cats = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM cats'):
        cat = cat_from_row(row)
        cats.append(cat)
    con.close()
    return cats

def get_litters():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    list = []
    litters = cur.execute('SELECT * FROM litters').fetchall()
    for litter in litters:
        print(litter[0],litter[1])
        father = get_cat_by_id(litter[0])
        mother = get_cat_by_id(litter[1])
        date = litter[2]
        kittens = [kitten[0] for kitten in cur.execute('SELECT kitten FROM belongs WHERE mother = ? AND father = ? AND birthdate = ?', (litter[0], litter[1], date)).fetchall()]
        list.append({'mother': mother, 'father':father, 'birthdate':date, 'kittens':kittens})
    return list

def get_litter(mother, father, date):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    litter = cur.execute('SELECT * FROM litters WHERE mother = ? AND father = ? AND birthdate = ?', (mother, father, date)).fetchone()
    kittens = [kitten[0] for kitten in cur.execute('SELECT kitten FROM belongs WHERE mother = ? AND father = ? AND birthdate = ?', (mother, father, date)).fetchall()]
    con.close()
    return {'mother':litter[1], 'father':litter[0], 'birthdate':litter[2], 'born':litter[3], 'kittens': kittens}

def get_breeding_cats():
    cats = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM cats WHERE breeding=1'):
        cat = cat_from_row(row)
        cats.append(cat)
    con.close()
    return cats

#litter 
def create_litter(mother, father, date):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    check = cur.execute("SELECT * FROM litters WHERE mother=? AND father=? AND birthdate=?", (mother, father, date)).fetchone()
    if not check:
        cur.execute("INSERT INTO litters(mother, father, birthdate), VALUES(?,?,?)", (mother, father, date))
        con.commit()
        con.close()
        return 1
    con.close()
    return 0

def delete_litter(mother, father, date):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    check = cur.execute("SELECT * FROM litters WHERE mother=? AND father=? AND birthdate=?", (mother, father, date)).fetchone()
    if check:
        cur.execute("DELETE FROM litters WHERE mother=? AND father=? AND birthdate=?", (mother, father, date))
        con.commit()
        con.close()
        return 1
    con.close()
    return 0

def add_kitten_to_litter(mother, father, kitten, date):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("INSERT INTO belongs(mother, father, kitten, birthdate) VALUES (?, ?, ?, ?)", (mother, father, kitten, date))
    con.commit()
    con.close()


def remove_kitten_from_litter(mother, father, kitten, date):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("DELETE FROM belongs WHERE mother=? AND father=? AND birthdate=? AND kitten=?", (mother, father, date, kitten))
    con.commit()
    con.close()


def update_litter(mother, father, birthdate, new_date, born, public):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("UPDATE litters SET birthdate=?, born=?, public=? WHERE mother = ? AND father=? AND birthdate = ?", (new_date, born, public, mother, father, birthdate))
    con.commit()
    con.close()

#cat
def delete_cat(id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("DELETE FROM cats WHERE id=?", (id,))
    con.commit()
    con.close()

def update_cat(cat):
    print("UPDATE HAPENNED")
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("UPDATE cats SET sex=?, color=?, about=?, forsale=?, picture=?, breeding=?, birthdate=?, sold=? WHERE catname=?", (cat.sex, cat.color, cat.description, cat.forsale, cat.picture, cat.breeding, cat.birthdate, cat.sold, cat.name))
    con.commit()
    con.close()

def create_cat(cat):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    print("CREATING A CAT")
    cur.execute("INSERT INTO cats(sex, color, about, forsale, picture, breeding, birthdate, sold, catname) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (cat.sex, cat.color, cat.description, cat.forsale, cat.picture, cat.breeding, cat.birthdate, cat.sold, cat.name))
    con.commit()
    con.close()
    

def cat_from_row(row):
    name = row[2]
    sex = row[3]
    color = row[4]
    about = row[5]
    forsale = row[6]
    picture = row[7]
    breeding = row[8]
    birthdate = datetime.datetime.strptime(row[9], "%Y-%m-%d")
    sold = row[10]
    
    cat = Cat(name, birthdate, color, sex, about, picture, forsale, breeding, sold)
    return cat