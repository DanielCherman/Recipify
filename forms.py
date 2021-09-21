from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, IntegerField)
from wtforms.validators import (DataRequired, Length, Optional, InputRequired, EqualTo)


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           Length(min=5, max=16)])
    password = PasswordField('Password', validators=[DataRequired(),
                             Length(min=5, max=100)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           Length(min=5, max=16)])
    password = PasswordField('Password', validators=[DataRequired(),
                             Length(min=5, max=100),
                             EqualTo('confirm',
                             message="Passwords must match")])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')


class Recipe(FlaskForm):
    recipe_name = StringField('Recipe Name:', [InputRequired()])
    recipe_type = StringField('Recipe Type:', [InputRequired()])
    recipe_desc = StringField('Description:', [InputRequired()])
    serving = IntegerField('Serving Size:', [InputRequired()])
    prep_time = IntegerField('Preparation Time:', [InputRequired()])
    cook_time = IntegerField('Cooking Time:', [InputRequired()])
    img_url = StringField('Photo link:', [Optional()])
    submit = SubmitField('Add Recipe')
