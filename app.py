from flask import Flask, render_template, flash, session, request, redirect, url_for, make_response

app = Flask(__name__)

# Секретний ключ потрібний для flash-повідомлень та сесій (додам пізніше)
app.secret_key = 'super_secret_key_for_koroliuk'

@app.route('/')
def resume():

    return render_template('resume.html', title="My Resume")


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Contacts")

if __name__ == '__main__':
    app.run(debug=True)