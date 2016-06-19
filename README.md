The execution meal is a lightweight application that enables 
visitors to log and share the last meals they'd want to eat on earth.


# ############################################################ INSTALLATION
[ sudo easy_install pip ]
[ sudo pip install virtualenv ]
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
export EXECUTIONMEAL_SETTINGS=/Users/mars/code/executionmeal/executionmeal/settings.cfg
? [initialize db, see below]
python runserver.py


Notes:
? sqlite3 /tmp/executionmeal.db < executionmeal/schema.sql 		# Will create a database table if one doesnt exist
[] Optional Steps

# ############################################################ NOTES

- Application is structured after  http://flask.pocoo.org/docs/0.11/patterns/packages/


