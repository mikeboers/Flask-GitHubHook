from flask import url_for, request, redirect
from flask.ext.githubhook.core import do_post
from flask.ext.mako import TemplateError

from githubhookapp.core import app
from githubhookapp.logs import setup_logs
from githubhookapp.worker import start_worker


setup_logs(app)


# Register this again, since that is what I have set on all my repos by hand.
app.route('/', methods=['POST'])(do_post)


@app.errorhandler(TemplateError)
def handle_mako_error(e):
    if app.debug:
        return e.text, 500, [('Content-Type', 'text/plain')]


import githubhookapp.auth
import githubhookapp.views
start_worker()
