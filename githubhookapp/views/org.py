import json

import requests

from . import *


@app.route('/org/<login>', endpoint='org')
def org(login):
    org = github_api('orgs/%s' % login)
    repos = github_api('orgs/%s/repos' % login)
    repo_hooks = dict(
        (repo['name'], github_api('repos/%s/%s/hooks' % (login, repo['name'])))
        for repo in repos
    )
    return render_template('org.html',
        org=org,
        repos=repos,
        repo_hooks=repo_hooks,
    )

@app.route('/org/<login>/<name>/add_hook')
def add_hook(login, name):

    hook_url = request.host_url.rstrip('/') + url_for('githubhook.post')
    res = requests.post('https://api.github.com/repos/%s/%s/hooks' % (login, name), data=json.dumps({
        'name': 'web',
        'config': {
            'url': hook_url,
            'content_type': 'form',
        }, 
    }))
    return res.text
