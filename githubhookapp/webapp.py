from flask import url_for, request
from flask.ext.githubhook.core import do_post

from githubhookapp.core import app
from githubhookapp.logs import setup_logs
from githubhookapp.worker import start_worker


setup_logs(app)


@app.route('/')
def do_index():
    return '<pre>Add the following hook to your repos: <strong>%s%s' % (
        request.host_url.rstrip('/'),
        url_for('githubhook.post'),
    )


# Register this again, since that is what I have set on all my repos by hand.
app.route('/', methods=['POST'])(do_post)


import githubhookapp.auth
import githubhookapp.views
start_worker()
