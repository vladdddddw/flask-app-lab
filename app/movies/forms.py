from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class MovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)])
    year = IntegerField("Year", validators=[Optional(), NumberRange(min=1880, max=2100)])
    rating = FloatField("Rating (0-10)", validators=[Optional(), NumberRange(min=0, max=10)])
    genre_id = SelectField("Genre", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save")
