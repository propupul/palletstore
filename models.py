basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI']=\
'sqlite:///' + os.path.join(basedir, 'sqlite_product_location')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


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
        return('The location is %s' % self.location)
