import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
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
app.config['SECRET_KEY'] = 'some very hard to guess key'

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

    def __repr__(self):
        return '<StoreRetrieve %r>' % self.location


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

    def __repr__(self):
        return '<User %r>' % self.username


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
@app.route('/')
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
        if older_date.date <= str(date.today()) and request.method == 'POST':
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
''''Retrieve Page: Retrieves the selected product with the oldest date. stored the NameForm object in the "form" variable. "order" variable holds StoreRetrieve which is the name of the database model, imorted from database_config.py which sets up the initial configuration using flask-sqlalchemy. "order" object variable queries the entire list of products in their location, filtered by selected proudct, and ordered by date. "older_date" object variable queries the first item/sku/product in the list by selected product, and by date. for "item" in "order" iterates through the entire list of products using "item" as the index variable. if "older_date.date" is less than today's date and the "request.method" is equals to 'POST' then create a "perma_date" variable containing the "older_date.date" object. Make the "older_date.sku" an "Empty" string, and the "older.date.date" a "N/A" string as well. Add and commit the session to the table. Used flask-bootstrap and give the user a "flash" message which displays the product name and its store date. If locations are full display a "there are no more pallets avialble to retrieve DEBUG" thats' a debug for me.  '''


# Third route store page
@app.route('/store', methods=['GET', 'POST'])
@login_required
def store():
    form = NameForm()
    view = StoreRetrieve.query.all()
    for item in view:
        sku_search = StoreRetrieve.query.filter_by(sku='Empty').first()
        try:
            if sku_search.sku == 'Empty' and request.method == 'POST':
                sku_search.sku = form.select.data
                sku_search.date = date.today()
                db.session.add(sku_search)
                db.session.commit()
                flash('STORE IT AT: %s' % sku_search.location)
                return redirect(url_for('store'))
        except:
            if request.method == 'POST':
                flash('Locations are full')
                return redirect(url_for('store'))
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
    manager.run()
    #app.run(host='0.0.0.0')
