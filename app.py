from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, date
from models import StoreRetrieve, db
from nameform import NameForm
'''Imported modules'''

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
'''Boiler Plate'''

app.config['SECRET_KEY'] = 'some very hard to guess key'
'''SECRET_KEY will be moved'''


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', current_time=datetime.utcnow()), 500
'''Two error pages '''


@app.route('/')
def index():
    order = StoreRetrieve.query.order_by(StoreRetrieve.date).all()
    return render_template('index.html', current_time=datetime.utcnow(),
                           order=order)


@app.route('/retrieve', methods=['GET', 'POST'])
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
            flash('There are no more %s pallets available to retrieve DEBUG'
                  % form.select.data)
            return(redirect(url_for('retrieve')))
    return render_template('retrieve.html',
                           current_time=datetime.utcnow(), form=form)
''''Retrieve Page: Retrieves the selected product with the oldest date. stored the NameForm object in the "form" variable. "order" variable holds StoreRetrieve which is the name of the database model, imorted from database_config.py which sets up the initial configuration using flask-sqlalchemy. "order" object variable queries the entire list of products in their location, filtered by selected proudct, and ordered by date. "older_date" object variable queries the first item/sku/product in the list by selected product, and by date. for "item" in "order" iterates through the entire list of products using "item" as the index variable. if "older_date.date" is less than today's date and the "request.method" is equals to 'POST' then create a "perma_date" variable containing the "older_date.date" object. Make the "older_date.sku" an "Empty" string, and the "older.date.date" a "N/A" string as well. Add and commit the session to the table. Used flask-bootstrap and give the user a "flash" message which displays the product name and its store date. If locations are full display a "there are no more pallets avialble to retrieve DEBUG" thats' a debug for me.  '''


@app.route('/store', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
