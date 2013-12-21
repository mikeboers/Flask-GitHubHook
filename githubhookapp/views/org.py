import json

import requests

from . import *


@app.route('/org/<login>', endpoint='org')
def org(login):
    org = github_get('orgs/%s' % login)
    repos = github_get('orgs/%s/repos' % login)
    repo_hooks = dict(
        (repo['name'], github_get('repos/%s/%s/hooks' % (login, repo['name'])))
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
    res = github_post('repos/%s/%s/hooks' % (login, name),
        name='web',
        config={
            'url': hook_url,
            'content_type': 'form',
        },
        events=['push'],
        active=True,
    )
    return json.dumps(res, indent=4, sort_keys=True)
