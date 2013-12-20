from flask import url_for, request
from flask.ext.githubhook.core import do_post

from .core import app
from .logs import setup_logs


setup_logs(app)


@app.route('/')
def do_index():
    return '<pre>Add the following hook to your repos: <strong>%s%s' % (
        request.host_url.rstrip('/'),
        url_for('githubhook.post'),
    )

@app.route('/', methods=['POST'])
def do_redirect():
    return redirect(url_for('githubhook.post'), code=307)

