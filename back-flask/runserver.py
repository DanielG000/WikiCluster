from Wiki import app
import os


app.run(host=os.environ['BACKEND_HOST'], port=os.environ['BACKEND_PORT'])

