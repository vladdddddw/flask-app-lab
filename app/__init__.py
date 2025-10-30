from flask import Flask
import logging

app = Flask(__name__)

app.secret_key = 'super_secret_key_for_koroliuk'
from app.users.views import users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from app.products.views import products_bp
app.register_blueprint(products_bp, url_prefix='/products')

logging.basicConfig(filename='contact_submissions.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s')
from app import views