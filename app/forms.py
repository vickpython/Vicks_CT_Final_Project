from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import PasswordField, BooleanField
from flask_wtf import FlaskForm

class StockTickerForm(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    expiration_date = StringField('Expiration Date', validators=[DataRequired()])
    strike_price = StringField('Strike Price', validators=[DataRequired()])
    submit = SubmitField()
    
class UserInfoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField() 

    