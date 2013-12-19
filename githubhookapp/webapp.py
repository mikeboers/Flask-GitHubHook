from flask import url_for, request, redirect

from .core import app


@app.route('/')
def do_index():
    return '<pre>Add the following hook to your repos: <strong>%s%s' % (
        request.host_url.rstrip('/'),
        url_for('githubhook.post'),
    )

@app.route('/', methods=['POST'])
def do_redirect():
    return redirect(url_for('githubhook.post'), code=307)

