from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):

    name = StringField('Your Name', validators=[
        DataRequired(message="Будь ласка, введіть ваше ім'я."),
        Length(min=3, max=20, message="Ім'я повинно бути від 3 до 20 символів.")
    ])

    email = StringField('Your Email', validators=[
        DataRequired(message="Будь ласка, введіть email."),
        Email(message="Некоректний формат email.")
    ])

    phone = StringField('Phone (Optional)', validators=[
        Regexp(r'^\+380\d{9}$', message="Формат телефону: +380XXXXXXXXX.")
    ])

    subject = SelectField('Reason for Contact', choices=[
        ('question', 'General Question'),
        ('feedback', 'Website Feedback'),
        ('other', 'Other')
    ], validators=[DataRequired()])

    message = TextAreaField('Your Message', validators=[
        DataRequired(message="Поле повідомлення не може бути порожнім."),
        Length(max=1000, message="Повідомлення занадто довге (макс. 1000 символів).")
    ])

    submit = SubmitField('Send Message')

class LoginForm(FlaskForm):


    username = StringField('Username', validators=[
        DataRequired(message="Ім'я користувача не може бути порожнім.")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message="Будь ласка, введіть пароль."),
        Length(min=5, max=15, message="Пароль має бути від 5 до 15 символів.")
    ])

    remember = BooleanField("Keep me logged in")

    submit = SubmitField('Log In')