from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,FloatField
from wtforms.validators import DataRequired,length,Email, Optional

class PriceForm(FlaskForm):
    
    min = FloatField("min price",validators= [Optional()])
    max = FloatField("max price",validators= [Optional()])
    submit = SubmitField("Done")

class RegisterForm(FlaskForm):
    
    email = StringField("email", validators=[DataRequired(),Email()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), length(min=5, max=64)])

    submit = SubmitField("sign in")

class LoginForm(FlaskForm):
    
    email = StringField("email", validators=[DataRequired(),Email()])
    password = PasswordField("password", validators=[DataRequired(), length(min=5, max=64)])

    login = SubmitField("login")