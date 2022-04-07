import sqlite3
import app.models as models
from werkzeug.security import generate_password_hash, check_password_hash

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO cats (catname, sex) VALUES (?, ?)",
            ('Fluffone', 'female')
            )

cur.execute("INSERT INTO cats (catname, sex) VALUES (?, ?)",
            ('Beaker', 'female')
            )

#set up user object
silvia = models.User('silvia', 'silvia@gmail.com')
silvia.set_password('password')
hash = silvia.password_hash
print(check_password_hash(hash, 'password'))
print(silvia.name, silvia.email, hash)

#insert
cur.execute("INSERT INTO users (username, email, pwhash) VALUES (?, ?, ?)",
            (silvia.name, silvia.email, hash))
dbhash = cur.execute("SELECT pwhash FROM users WHERE username='silvia'").fetchone()[0]

#tests
print(dbhash,hash)
print(check_password_hash(dbhash, 'password'))
print(dbhash == hash)

connection.commit()
connection.close()
