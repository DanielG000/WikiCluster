from flask import Flask 
from Wiki.config import *

app = Flask(__name__)
app.config.from_object(DevConfig)

from Wiki.routes import *
