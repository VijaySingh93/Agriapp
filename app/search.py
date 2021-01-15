from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class searchAnswers(FlaskForm):
    searchtext = StringField('',
                             validators=[DataRequired()])
    submit = SubmitField('Search')
