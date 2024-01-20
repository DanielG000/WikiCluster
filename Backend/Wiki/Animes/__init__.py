from flask import Blueprint

Animes = Blueprint('Animes', __name__)

from . import routes