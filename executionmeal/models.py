import sqlite3
from flask import Flask, g
from executionmeal import app
 
# SQL Alchemy Code

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

"""
from executionmeal import models
from executionmeal.models import db
from executionmeal.models import Entry
db.create_all()
john = Entry('self', 'john', 'beer', 'apple juice', 'toast', 'steak', 'french fries', 'salad', 'apple pie' 'electrocution', 'image.png')
bill = Entry('self', 'bill', 'beer', 'apple juice', 'toast', 'steak', 'french fries', 'salad', 'apple pie' 'electrocution', 'image.png')

db.session.add(john)
db.session.add(bill)
db.session.commit()
entries = Entry.query.all()

"""
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    drink_non_alcoholic = db.Column(db.Text)
    drink_alcoholic = db.Column(db.Text)
    appetizer = db.Column(db.Text)
    entree = db.Column(db.Text)
    side_1 = db.Column(db.Text)
    side_2 = db.Column(db.Text)
    dessert = db.Column(db.Text)
    how_die = db.Column(db.Text)
    image_name = db.Column(db.Text)


    def __init__(self, first_name, drink_non_alcoholic, drink_alcoholic, appetizer, entree, side_1, side_2, dessert, how_die, image_name):
    #def __init__(first_name, drink_non_alcoholic, drink_alcoholic, appetizer, entree, side_1, side_2, dessert, how_die, image_name):
        self.first_name = first_name
        self.drink_non_alcoholic = drink_non_alcoholic
        self.drink_alcoholic = drink_alcoholic
        self.appetizer = appetizer
        self.entree = entree
        self.side_1 = side_1
        self.side_2 = side_2
        self.dessert = dessert
        self.how_die = how_die
        self.image_name = image_name

    def __repr__(self):
        return '<id %r>' % self.id



##########

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


