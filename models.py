from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate, MigrateCommand
from startup import app, basedir, os
from flask_script import Manager, Shell
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'sqlite_product_location')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 
class StoreRetrieve(db.Model):
    __tablename__ = 'Store_Retrieve'
    location = db.Column(db.String(80), primary_key=True, unique=True)
    sku = db.Column(db.String(80))
    date = db.Column(db.String(80))

    def __init__(self, location, sku, date):
        self.location = location
        self.sku = sku
        self.date = date

    def __repr__(self):
        return 'The location is %s' % self.location




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
