from flask import Flask


app = Flask(__name__)

app.secret_key = 'super_secret_key_for_koroliuk'



from app import views