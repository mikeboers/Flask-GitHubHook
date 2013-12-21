import json
import os
import shelve

import requests
from flask import Flask, session
from flask.ext.mako import MakoTemplates
from flask.ext.githubhook import GitHubHook
from memoize import Memoizer


app = Flask(__name__, static_url_path='')
app.root_path = os.path.abspath(os.path.join(__file__, '..'))
app.instance_path = os.path.abspath(os.path.join(__file__, '..', '..', 'var'))

config_path = os.path.join(app.instance_path, 'config.py')
if os.path.exists(config_path):
    locals_ = {}
    execfile(config_path, locals_, app.config)
    app.config.update(locals_)
else:
    print 'Could not find var/config.py'

app.config['SECRET_KEY'] = app.config.get('SECRET_KEY') or 'monkey'

app.config['GITHUB_ALLOWED_OWNERS'] = set(['mikeboers', 'FluentImage'])
app.debug = app.debug or bool(os.environ.get('DEBUG'))

githubhook = GitHubHook(app=app, url_prefix='/hook')
mako = MakoTemplates(app)

memo = Memoizer({})


def github_get(method, **params):
    access_token = session.get('access_token')
    if not access_token:
        return
    return _github_api_get(method, access_token=access_token, **params)


@memo
def _github_api_get(method, **kwargs):
    return requests.get(
        'https://api.github.com/' + method.strip('/'),
        params=kwargs,
    ).json()


def github_post(method, **kwargs):
    access_token = session.get('access_token')
    if not access_token:
        return
    return requests.post(
        'https://api.github.com/' + method.strip('/'),
        data=json.dumps(kwargs),
        params={'access_token': access_token},
    ).json()
