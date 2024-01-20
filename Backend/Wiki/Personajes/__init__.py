from flask import Blueprint

Personajes = Blueprint('Personajes', __name__)

from . import routes