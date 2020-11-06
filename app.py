import os # Python standard library
from datetime import datetime, date # Python standard library
from flask import Flask, render_template, url_for, redirect, request, flash # Main Flask modules
from flask_script import Manager, Shell # Library no longer maintained and will be removed
from flask_bootstrap import Bootstrap # Bootstrap plugin
from flask_moment import Moment # This extension enhances Jinja2 templates with formatting of dates and times using moment.js.
from flask_sqlalchemy import SQLAlchemy # Adds support for SQLAlchemy
from flask_migrate import Migrate, MigrateCommand # Handles SQLAlchemy database migrations for Flask applications using Alembic.
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from nameform import NameForm, LoginForm
'''Imported modules'''

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask object
app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'sqlite_product_location')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'lflkajsdlkfjsadk;ldklfjsakl;fjslajitrjiwj'

# Flask plugin objects take 'app' object as a param.
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


# Models
class StoreRetrieve(db.Model):
    __tablename__ = 'Store_Retrieve'
    location = db.Column(db.String(80), primary_key=True, unique=True)
    sku = db.Column(db.String(80))
    date = db.Column(db.String(80))

#    def __init__(self, location, sku, date):
#        self.location = location
#        self.sku = sku
#        self.date = date

    #def __repr__(self):
        #return '<StoreRetrieve %r>' % self.location

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #def __repr__(self):
        #return '<User %r>' % self.username


# Imports 4 objects for the database.
def make_shell_context():
    return dict(app=app, db=db, StoreRetrieve=StoreRetrieve, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))


# Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', current_time=datetime.utcnow()), 500
'''Two error pages '''


# First route index page
@app.route('/index')
@login_required
def index():
    order = StoreRetrieve.query.order_by(StoreRetrieve.date).all()
    return render_template('index.html', current_time=datetime.utcnow(),
                           order=order)


# Second route retrieve page
@app.route('/retrieve', methods=['GET', 'POST'])
@login_required
def retrieve():
    form = NameForm()
    order = StoreRetrieve.query.filter_by(sku=form.select.data).order_by(StoreRetrieve.date).all()
    older_date = StoreRetrieve.query.filter_by(sku=form.select.data).order_by(StoreRetrieve.date).first()
    for item in order:
        print('for item executes')
        print(older_date)
        if request.method == 'POST':
            perma_date = older_date.date
            older_date.sku = 'Empty'
            older_date.date = 'N/A'
            db.session.add(older_date)
            db.session.commit()
            flash('Product Name: %s - Location: %s Store date: %s'
                  % (form.select.data, older_date.location, perma_date))
            return(redirect(url_for('retrieve')))
            flash('more {} pallets available to retrieve'.format(form.select.data))
            return(redirect(url_for('retrieve')))
    return render_template('retrieve.html',
                           current_time=datetime.utcnow(), form=form)
''''Retrieve Page: Retrieves the selected product with the oldest date. I stored the "NameForm" object in the "form" variable. "order" variable holds "StoreRetrieve" which is the name of the database model, 
imported from database_config.py which sets up the initial configuration using flask-sqlalchemy. "order" object variable queries the entire list of products in their location, 
filtered by selected product, and ordered by date. "older_date" object variable queries the first item/sku/product in the list by selected product, and by date. 
for "item" in "order" iterates through the entire list of products using "item" as the index variable. 
if "older_date.date" is less than today's date and the "request.method" is equals to 'POST' then create a "perma_date" variable containing the "older_date.date" object. 
Make the "older_date.sku" an "Empty" string, and the "older.date.date" a "N/A" string as well.
Add and commit the session to the table. Used flask-bootstrap and give the user a "flash" message which displays the product name and its store date. 
If locations are full display a "there are no more pallets available to retrieve DEBUG" thats' a debug for me. '''


# Third route store page
@app.route('/store', methods=['GET', 'POST'])
@login_required
def store():
    top_location = [] # Top locations stored here (i.e A1-3R, A1-3L)
    remaining_location = [] # Remaining locations stored here
    protected_location = ['A8-3LS', 'A8-3RS', 'A9-3LS', 'A9-3RS', 'A12-3LS', 'A12-3RS', 'A13-3LS', 'A13-3RS'] # This location list must be full before accessing third level locations
    third_level_s = [] # Third level location that are not racked
    heavy_pallets = ['464 50lbs banded', '444 50lbs', '464 50lbs', '464 10lbs', '444 10lbs']

    form = NameForm() # instance of NameForm() object
    view = StoreRetrieve.query.filter(StoreRetrieve.sku.startswith('Empty')).all() # view is a 'list' type containing all the 'Empty' skus available
    for item in view: # objects inside the 'view' list are classes with ['date', 'location', 'metadata', 'query', 'query_class', 'sku'] usable methods (i.e item.sku, item.date)
        end_L = item.location.endswith('3L')
        end_R = item.location.endswith('3R')
        end_LS = item.location.endswith('3LS')
        end_RS= item.location.endswith('3RS')
        # print('This is end_L boolean: ', end_L)
        # print('This is end_R boolean: ', end_R)
        # print('Start For loop')
        if end_L or end_R: # If either end_L or end_R are true run the code below. They should end in 3L or 3R
            sku_search = StoreRetrieve.query.filter_by(location=item.location).first() # sku_search is a class type object with the following method [date', 'location', 'metadata', 'query', 'query_class', 'sku'] printing the first item filtered by location
            top_location.append(sku_search.location) # This will append all the locations ending in 3L or 3R in the top_location list
            # print('first IF')
            # print(top_location)

        if end_RS or end_LS:
            sku_search = StoreRetrieve.query.filter_by(location=item.location).first()
            third_level_s.append(sku_search.location)
            print(third_level_s)

        if not end_L and not end_R: # if end_L == 'False' and end_R == 'False' only then run the code below, and append to remaining_location list the locations that do not end in either 3L or 3R
            sku_search = StoreRetrieve.query.filter_by(location=item.location).first()
            remaining_location.append(sku_search.location)
            # print("Ends with 3L:", end_L)
            # print(sku_search.location)
            # print("Ends with 3R:", end_R)
            # print(sku_search.location)
            # print('Second If')
    if end_RS or end_LS in remaining_location:
        for location in third_level_s:
            remaining_location.remove(location)
    print(remaining_location)


    try:
        if request.method == 'POST' and not remaining_location and  form.select.data not in heavy_pallets:
            sku_search = StoreRetrieve.query.filter_by(location=third_level_s[0]).first()
            sku_search.sku = form.select.data
            flash('SKU {}'.format(sku_search.sku))
            sku_search.date = date.today()
            flash("Today's date: {}".format(sku_search.date))
            flash("Location: {}".format(sku_search.location))
            db.session.add(sku_search)
            db.session.commit()
            flash('First Try')
            return redirect(url_for('store'))

    except:
        #flash('ERROR!!')
        print(remaining_location)


    try:
        if request.method == 'POST' and (form.select.data == '464 10lbs' or form.select.data == '444 10lbs'):
            sku_search = StoreRetrieve.query.filter_by(location=top_location[0]).first()
            sku_search.sku = form.select.data
            flash('SKU {}: '.format(sku_search.sku))
            sku_search.date = date.today()
            flash("Today's date: {}".format(sku_search.date))
            flash("Location: {}".format(sku_search.location))
            db.session.add(sku_search)
            db.session.commit()
            flash('Second Try')
            return redirect(url_for('store'))

    except:
        if request.method =='POST' and not top_location:
            #fix remaining_locatin[0] running out of index inside an except use a 'finally'
            flash('Top locations are full')
            sku_search = StoreRetrieve.query.filter_by(location=remaining_location[0]).first()
            sku_search.sku = form.select.data
            flash('SKU {}: '.format(sku_search.sku))
            sku_search.date = date.today()
            flash("Today's date: {}".format(sku_search.date))
            flash("Location: {}".format(sku_search.location))
            db.session.add(sku_search)
            db.session.commit()
            return redirect(url_for('store'))
    finally:
        if not top_location and not remaining_location:
            flash('All locations are full!!')

    try:
        if request.method == 'POST' and form.select.data != '464 10lbs' and (top_location or not top_location):
            sku_search = StoreRetrieve.query.filter_by(location=remaining_location[0]).first()
            sku_search.sku = form.select.data
            flash('SKU: {}'.format(sku_search.sku))
            sku_search.date = date.today()
            flash("Today's date: {}".format(sku_search.date))
            flash("Location: {}".format(sku_search.location))
            db.session.add(sku_search)
            db.session.commit()
            flash('Third Try')
            return redirect(url_for('store'))
    except:
        if not top_location and not remaining_location and not third_level_s:
            flash('All locations are full')

    return render_template('store.html', view=view,
                           current_time=datetime.utcnow(), form=form)


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash("Invalid username or password")
    return render_template('login.html', form=form, current_time=datetime.utcnow())


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5000)
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)