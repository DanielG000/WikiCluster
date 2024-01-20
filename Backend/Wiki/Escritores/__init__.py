from flask import Blueprint

Escritores = Blueprint('Escritores', __name__)

from . import routes
