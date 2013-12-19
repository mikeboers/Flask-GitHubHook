import os

from flask import Flask
from flask.ext.githubhook import GitHubHook

app = Flask(__name__)
app.root_path = os.path.abspath(os.path.join(__file__, '..', '..'))
app.instance_path = os.path.join(app.root_path, 'var')

app.config['GITHUB_ALLOWED_OWNERS'] = set(['mikeboers', 'FluentImage'])
app.debug = app.debug or bool(os.environ.get('DEBUG'))

githubhook = GitHubHook(app=app, url_prefix='/hook')

