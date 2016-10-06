from flask import Flask, render_template, url_for, redirect, request
from flask import flash
# from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from datetime import datetime, date
from database_config import PrimaryView, db, basedir
from wtforms import SubmitField, SelectField
# from wtforms.validators import Required
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


app.config['SECRET_KEY'] = 'wq3hnf}RY4v3D864=ZZ@B8]ikF[KEC[(x8,4W%azvLNbHos2.s'

app.config['SQLALCHEMY_DATABASE_URI']=\
'sqlite:////' + os.path.join(basedir, 'sqlite_product_location')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


class NameForm(Form):
    select = SelectField('Select Product', choices=[('464 50lbs', '464 50lbs'),
                         ('444 50lbs', '444 50lbs'), ('464 50lbs banded', '464 50lbs banded'), ('464 10lbs', '464 10lbs'), ('8oz Mason', '8oz Mason'), ('4oz Jelly', '4oz Jelly'), ('6oz Tin 120', '6oz Tin 120'), ('4oz Tin 120', '4oz Tin 120'), ('Soy Candle Making Kit', 'Soy Candle Making Kit'), ('4oz candle tin 12pc', '4oz candle tin 12pc'), ('8oz Mason MP', '8oz Mason MP')])
    submit = SubmitField('Save')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return (render_template('500.html', current_time=datetime.utcnow()), 500)


@app.route('/')
def index():
    order = PrimaryView.query.order_by(PrimaryView.date).all()
    return (render_template('index.html',
                           current_time=datetime.utcnow(), order=order))


# The /retrieve will use Post method
@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    form = NameForm()
    order = PrimaryView.query.filter_by(sku=form.select.data).order_by(PrimaryView.date).all()
    individual_date = PrimaryView.query.filter_by(sku=form.select.data).order_by(PrimaryView.date).first()
    for item in order:
        if individual_date.date <= str(date.today()) and request.method == 'POST':
            oldest = PrimaryView.query.filter_by(sku=form.select.data).order_by(PrimaryView.date).first()
            perma_date = oldest.date
            oldest.sku = 'Empty'
            oldest.date = 'N/A'
            db.session.add(oldest)
            db.session.commit()
            flash('Product Name: %s - Location: %s Store date: %s' % (form.select.data, oldest.location, perma_date))
            return(redirect(url_for('retrieve')))
            flash('There are no more %s pallets available to retrieve DEBUG' % form.select.data)
            return(redirect(url_for('retrieve')))
    return (render_template('retrieve.html',
                            current_time=datetime.utcnow(), form=form))


@app.route('/store', methods=['GET', 'POST'])
def store():
    form = NameForm()
    view = PrimaryView.query.all()
    for item in view:
        if item.sku == 'Empty' and request.method == 'POST':
            sku_search = PrimaryView.query.filter_by(sku='Empty').first()
            sku_search.sku = form.select.data
            sku_search.date = date.today()
            db.session.add(sku_search)
            db.session.commit()
            flash('STORE IT AT: %s' % item.location)
            return(redirect(url_for('store')))
    return(render_template('store.html', view=view,
                           current_time=datetime.utcnow(), form=form))

if __name__ == '__main__':
    app.run(debug=True)
