from app import app
from app.models import Cat, Litter
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
        print(litter)
        father = get_cat_by_name(litter[0])
        mother = get_cat_by_name(litter[1])
        birthdate = litter[2]
        duedate = litter[3]
        born = litter[4]
        public = litter[5]
        print("LITTER DATA")
        print(litter[0], litter[1], birthdate, born, public)
        kittens = [kitten[0] for kitten in cur.execute('SELECT kitten FROM belongs WHERE mother = ? AND father = ? AND birthdate = ?', (litter[1], litter[0], birthdate)).fetchall()]

        list.append(Litter(mother, father, birthdate, duedate, public, born, kittens))
    return list

def get_litter(mother, father, duedate, birthdate):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    litter = cur.execute("SELECT * FROM litters WHERE mother = ? AND father = ? AND duedate = ?", (mother, father, duedate)).fetchone()
    kittens = [kitten[0] for kitten in cur.execute('SELECT kitten FROM belongs WHERE mother = ? AND father = ? AND birthdate = ?', (mother, father, birthdate)).fetchall()]
    con.close()

    father = litter[0]
    mother = litter[1]
    duedate =  datetime.datetime.strptime(litter[2], "%Y-%m-%d")
    birthdate =  datetime.datetime.strptime(litter[3], "%Y-%m-%d")
    born = litter[4]
    public = litter[5]
    return Litter(mother, father, duedate, birthdate, born, public, kittens)

def get_expecting_litters():
    litters = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM litters WHERE born=0 AND public=1")
    for litter in rows:
        father = litter[0]
        mother = litter[1]
        duedate =  datetime.datetime.strptime(litter[2], "%Y-%m-%d")
        birthdate =  datetime.datetime.strptime(litter[3], "%Y-%m-%d")
        born = litter[4]
        public = litter[5]
        kittens = [kitten[0] for kitten in cur.execute('SELECT kitten FROM belongs WHERE mother = ? AND father = ? AND birthdate = ?', (litter[1], litter[0], birthdate)).fetchall()]
        litters.append(Litter(mother, father, duedate, birthdate, born, public, kittens))
    return litters

def get_breeding_cats():
    cats = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM cats WHERE breeding=1'):
        cat = cat_from_row(row)
        cats.append(cat)
    con.close()
    return cats

def get_sold_cats():
    cats = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM cats WHERE sold=1'):
        cat = cat_from_row(row)
        cats.append(cat)
    con.close()
    return cats


def get_available_kittens():
    kittens = []
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    #get cats that are marked for sale
    rows = cur.execute("SELECT * FROM cats WHERE forsale=1")
    for row in rows:
        kitten = cat_from_row(row)
        kittens.append(kitten)
    con.close()
    return kittens

#litter 
def create_litter(mother, father, birthdate, duedate):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    check = cur.execute("SELECT * FROM litters WHERE mother=? AND father=? AND birthdate=? AND duedate=?", (mother, father, birthdate, duedate)).fetchone()
    if not check:
        if not birthdate:
            birthdate = duedate
        if born:
            born = 1
        else:
            born = 0
        if public:
            public = 1
        else:
            public = 0
        cur.execute("INSERT INTO litters(mother, father, birthdate, duedate, born, public) VALUES(?,?,?,?)", (mother, father, birthdate, duedate, born, public))
        con.commit()
        con.close()
        return 1
    con.close()
    return 0

def delete_litter(mother, father, duedate):
    print('DELETEING LITTER IN QUERY')
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    check = cur.execute("SELECT * FROM litters WHERE mother=? AND father=? AND duedate=?", (mother, father, duedate)).fetchone()
    if check:
        cur.execute("DELETE FROM litters WHERE mother=? AND father=? AND duedate=?", (mother, father, duedate))
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


def remove_kitten_from_litter(mother, father, kitten):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("DELETE FROM belongs WHERE mother=? AND father=? AND kitten=?", (mother, father, kitten))
    con.commit()
    con.close()


def update_litter(mother, father, birthdate, duedate, born, public):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    print("WE ARE TRYING TO UPDATE A LITTER HERE")
    print(born, public)
    if born:
        born = 1
    else:
        born = 0
    if public:
        public = 1
    else:
        public = 0
    cur.execute("UPDATE litters SET birthdate=?, born=?, public=? WHERE mother=? AND father=? AND duedate=?", (birthdate, born, public, mother, father, duedate))
    con.commit()
    con.close()

#cat
def delete_cat(name):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("DELETE FROM cats WHERE catname=?", (name,))

    cur.execute("DELETE FROM litters WHERE mother=?", (name,))
    cur.execute("DELETE FROM litters WHERE father=?", (name,))

    cur.execute("DELETE FROM belongs WHERE mother=?", (name,))
    cur.execute("DELETE FROM belongs WHERE father=?", (name,))
    cur.execute("DELETE FROM belongs WHERE mother=?", (name,))
    cur.execute("DELETE FROM belongs WHERE kitten=?", (name,))
    con.commit()
    con.close()

def update_cat(cat):
    print("UPDATE HAPENNED")
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    if cat.sold:
        cat.sold = 1
    else:
        cat.sold = 0
    if cat.breeding:
        cat.breeding = 1
    else:
         cat.breeding = 0
    if cat.forsale:
        cat.forsale = 1
    else:
        cat.forsale = 0
    cur.execute("UPDATE cats SET sex=?, color=?, about=?, forsale=?, picture=?, breeding=?, birthdate=?, sold=? WHERE catname=?", (cat.sex, cat.color, cat.description, cat.forsale, cat.picture, cat.breeding, cat.birthdate, cat.sold, cat.name))
    con.commit()
    con.close()

def create_cat(cat):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    print("CREATING A CAT")
    if cat.sold:
        cat.sold = 1
    else:
        cat.sold = 0
    if cat.breeding:
        cat.breeding = 1
    else:
         cat.breeding = 0
    if cat.forsale:
        cat.forsale = 1
    else:
        cat.forsale = 0
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