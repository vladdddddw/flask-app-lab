from flask import Blueprint

posts_bp = Blueprint(
    'posts',
    __name__,
    template_folder='templates/posts',
    static_folder='static'
)

from . import views
from . import models