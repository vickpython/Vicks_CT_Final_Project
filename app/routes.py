import csv
from app import app, db, Message
from flask import render_template, request, redirect, url_for, flash, session
from app.forms import StockTickerForm
from app.wrappers import Orats
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from flask import send_file
from config import basedir

from app.forms import UserInfoForm, LoginForm

from app.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    context = {
        'form': form
    }
    if request.method == 'POST' and form.validate():
        # Get Information
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
        # Create new instance of User
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash("You have successfully registered", 'success')

        return redirect(url_for('index'))
    return render_template('register.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # Query database for user with email
        user = User.query.filter_by(email=email).first()
        # If no user, flash incorrect credentials
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect Email/Password. Please try again', 'danger')
            return redirect(url_for('login'))
        # Log user in
        login_user(user, remember=form.remember_me.data)
        # Flash success message
        flash('You have successfully logged in', 'success')
        # redirect to index
        return redirect(url_for('index'))

    return render_template('login.html', **context)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))

@app.route('/users')
@login_required
def users():
    context = {
        'users': User.query.all()
    }
    return render_template('users.html', **context) 

@app.route('/')
def index():
    # items = {1:"Bread", 2:"Butter"}
    return render_template('index.html')


@app.route('/stocktickers', methods =['GET', 'POST'])
@login_required
def ticker():
    form = StockTickerForm()
    ticker_data = None
    if request.method == 'POST' and form.validate():
        ticker = form.ticker_symbol.data
        expirDate = form.expiration_date.data
        strike = form.strike_price.data
        stock_api = Orats()
        ticker_data = stock_api.get_ticker_info(ticker, expirDate, strike)
        session['ticker_data'] = ticker_data.__dict__
        print(ticker_data)
        # return redirect(url_for('index'))
    return render_template('stocktickers.html', form=form, ticker_data=ticker_data)



@app.route('/getPlotCSV', methods =['GET']) 
def plot_csv():
    print(session['ticker_data'])
    with open('tickerinfo.csv', 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, session['ticker_data'].keys())
        writer.writeheader()
        writer.writerow(session['ticker_data'])
    return send_file(basedir + '/tickerinfo.csv', attachment_filename='tickerinfo.csv', as_attachment=True)

