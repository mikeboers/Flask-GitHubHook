from flask.ext.mako import render_template
from githubhookapp.core import app

@app.route('/')
def index():
    return render_template('index.html')
