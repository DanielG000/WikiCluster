from flask import Blueprint

Mangas = Blueprint('Mangas', __name__)

from . import routes