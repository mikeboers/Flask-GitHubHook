from flask import session, request, redirect, url_for

from githubhookapp.core import app, github_get


@app.context_processor
def auth_context():
    return {
        'user': github_get('user') or {},
    }


@app.before_request
def auth_check():

    if 'access_token' in session:
        user = github_get('user')
        if (
            user['login'] not in app.config['GITHUB_ALLOWED_OWNERS'] and
            request.endpoint != 'not_authorized'
        ):
            return redirect(url_for('not_authorized'))
        return

    if request.endpoint not in ('login', 'github_login', 'github_callback', 'static'):
        return redirect(url_for('login'))
