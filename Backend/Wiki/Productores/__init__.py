from flask import Blueprint

Productores = Blueprint('Productores', __name__)

from . import routes