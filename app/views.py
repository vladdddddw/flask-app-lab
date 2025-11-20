from flask import render_template, flash, redirect, url_for
from app import app  
from app.forms import ContactForm  
import logging 

@app.route('/')
def resume():
    return render_template('resume.html', title="My Resume")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        logging.info(f"New contact submission from {name} ({email})")
        flash(f'Message received from {name}. We will contact you shortly!', 'success')
        return redirect(url_for('contacts'))

    return render_template('contacts.html', title="Contacts", form=form)
