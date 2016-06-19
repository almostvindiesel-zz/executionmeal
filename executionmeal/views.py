import sqlite3
import os
import random
import requests
import requests.packages.urllib3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,  jsonify
from contextlib import closing
from werkzeug.utils import secure_filename
requests.packages.urllib3.disable_warnings()
from executionmeal import app
from executionmeal import models

@app.route('/')
def show_entries():
    show_entries_sql = 'select id lastmeal_id, first_name, drink_non_alcoholic, drink_alcoholic, appetizer, \
                               entree, side_1, side_2, dessert, how_die, image_name \
                        from entries \
                        order by id desc'

    db = models.get_db()
    cur = db.execute(show_entries_sql)
    entries = cur.fetchall()   

    if session:
        if 'step3_complete' in session.keys():
            if session['step3_complete']:
                getty_images = call_getty_images_api(session['drink_non_alcoholic'])
            else:
                getty_images = None
        else:
            getty_images = None
    else:
        getty_images = None

    return render_template('show_entries.html', entries=entries, getty_images=getty_images)


@app.route('/lastmeal/<int:lastmeal_id>')
def show_last_meal(lastmeal_id):
    lastmeal_sql = 'select id lastmeal_id, first_name, drink_non_alcoholic, drink_alcoholic, appetizer, \
                           entree, side_1, side_2, dessert, how_die, image_name \
                    from entries \
                    where id = %s' % lastmeal_id
    db = models.get_db()
    cur = db.execute(lastmeal_sql)
    entries = cur.fetchall() 

    return render_template('show_lastmeal.html', entry=entries[0])


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    if request.form.get('first_name', None) and request.form.get('drink_non_alcoholic', None) and request.form.get('drink_alcoholic', None):
        session['first_name'] = request.form['first_name']
        session['drink_non_alcoholic'] = request.form['drink_non_alcoholic']
        session['drink_alcoholic'] = request.form['drink_alcoholic']
        session['step1_complete'] = True

    if request.form.get('appetizer', None) and request.form.get('entree', None) and request.form.get('side_1', None) and request.form.get('side_2', None):
        session['appetizer'] = request.form['appetizer']
        session['entree'] = request.form['entree']
        session['side_1'] = request.form['side_1']
        session['side_2'] = request.form['side_2']
        session['step2_complete'] = True

    if request.form.get('dessert', None) and request.form.get('how_die', None):
        session['dessert'] = request.form['dessert']
        session['how_die'] = request.form['how_die']
        session['step3_complete'] = True

    if request.form.get('lastmeal_image', None):  #'file' in request.files:
        session['image_name'] = request.form['lastmeal_image']

        """ 
        Previous code supported uploading, just requiring image selection at this point...
        UPLOAD_FOLDER = 'uploads/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = str(random.randint(10000,99999)) + file.filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        """

        db = models.get_db()
        cur = db.execute('insert into entries (first_name, drink_non_alcoholic, drink_alcoholic, appetizer, \
                        entree, side_1, side_2, dessert, how_die, image_name) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [
                     session['first_name'], 
                     session['drink_non_alcoholic'], 
                     session['drink_alcoholic'],
                     session['appetizer'],  
                     session['entree'],
                     session['side_1'],
                     session['side_2'],
                     session['dessert'],
                     session['how_die'],
                     session['image_name']
                     #file.filename
                     ])
        lastmeal_id = cur.lastrowid
        db.commit()

        #clear_session_form_variables()
        return redirect(url_for('show_last_meal', lastmeal_id=lastmeal_id))


    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            #flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    clear_session_form_variables()
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# !!! This is a similiar copy of the other endpoint until I can figure out how to configure python correctly
@app.route('/api/gettyimages')
def call_getty_images_api_web():

    search_term = request.args.get('query')

    # curl -X GET -H "Api-Key:kjpmyxpm33e2uzjxcuhcfgnr" https://api.gettyimages.com/v3/search/images?phrase=cats
    api_key = 'kjpmyxpm33e2uzjxcuhcfgnr';
    headers = {'Api-Key': api_key}

    getty_creative_search_url = 'https://api.gettyimages.com/v3/search/images/creative?page_size=5&orientations=square&phrase='
    request_url = getty_creative_search_url + search_term

    r = requests.get(request_url, headers=headers)

    json_response = r.json()
    images = json_response['images']
    uris = []

    for datums in images:
        display_sizes = datums['display_sizes']
        uris.append(display_sizes[0]['uri'])

    return r.text
    #return jsonify({'image_urls': uris})


# Helper Functions #############################################################################

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def clear_session_form_variables():
    session.pop("first_name", None)
    session.pop("drink_non_alcoholic", None)
    session.pop("drink_alcoholic", None)
    session.pop("appetizer", None)
    session.pop("entree", None)
    session.pop("side_1", None)
    session.pop("side_2", None)
    session.pop("dessert", None)
    session.pop("how_die", None)
    session['step1_complete'] = False
    session['step2_complete'] = False
    session['step3_complete'] = False


# API Endpoints #############################################################################

#@app.route('/api/gettyimages', methods=['GET'])
#@app.route('/api/gettyimages')
def call_getty_images_api(search_term):

    # curl -X GET -H "Api-Key:kjpmyxpm33e2uzjxcuhcfgnr" https://api.gettyimages.com/v3/search/images?phrase=cats
    api_key = 'kjpmyxpm33e2uzjxcuhcfgnr';
    headers = {'Api-Key': api_key}

    getty_creative_search_url = 'https://api.gettyimages.com/v3/search/images/creative?page_size=5&orientations=square&phrase='
    request_url = getty_creative_search_url + search_term

    r = requests.get(request_url, headers=headers)

    json_response = r.json()
    images = json_response['images']
    uris = []

    for datums in images:
        display_sizes = datums['display_sizes']
        uris.append(display_sizes[0]['uri'])

    return uris #jsonify({'image_urls': uris})

if __name__ == '__main__':
    app.run(debug=True)
