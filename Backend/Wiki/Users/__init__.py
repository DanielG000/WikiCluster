from flask import Blueprint

Users = Blueprint('Users', __name__)

from . import routes
