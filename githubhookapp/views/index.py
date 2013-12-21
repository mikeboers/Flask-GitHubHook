import json

from flask.ext.mako import render_template
from githubhookapp.core import app
from githubhookapp.github import api

@app.route('/')
def index():
    return render_template('index.html',
        user_orgs=api('user/orgs'),
    )


@app.route('/organization/<login>')
def org(login):
    return json.dumps(api('/orgs/%s/repos' % login), indent=4, sort_keys=True)
