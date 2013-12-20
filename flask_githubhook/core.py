import errno
import functools
import json
import logging
import os
from subprocess import call

from flask import Blueprint, request, current_app
from . import utils


log = logging.getLogger(__name__)


def require_from_github(func):
    @functools.wraps(func)
    def _require_from_github(*args, **kwargs):
        res = current_app._githubhook_ext.assert_remote_netmask()
        if res:
            return res
        return func(*args, **kwargs)
    return _require_from_github


blueprint = Blueprint('githubhook', __name__)


@blueprint.route('', endpoint='get', methods=['GET'])
@require_from_github
def do_get():
    return 'You must POST.'


@blueprint.route('', endpoint='post', methods=['POST'])
@require_from_github
def do_post():

    payload = json.loads(request.form['payload'])
    owner_name = payload['repository']['owner']['name']
    repo_name = payload['repository']['name']

    allowed_owners = current_app.config['GITHUB_ALLOWED_OWNERS']
    if allowed_owners is not None and owner_name not in allowed_owners:
        msg = 'owner %r not permitted' % owner_name
        log.warning(msg)
        return msg

    clone_dir = current_app.config['GITHUB_CLONE_DIR']
    if clone_dir is not None:

        local_path = os.path.join(clone_dir, owner_name, repo_name + '.git')
        remote_url = 'git@github.com:%s/%s.git' % (owner_name, repo_name)

        if not os.path.exists(local_path):
            os.makedirs(local_path)
            call(['git', 'clone', '--mirror', remote_url, local_path])
        else:
            call(['git', '--git-dir', local_path, 'fetch', 'origin'])

    for hook in current_app._githubhooks:
        hook(payload)

    return 'ok'


class GitHubHook(object):

    remote_netmask = utils.network_mask('192.30.252.0', 22)

    def __init__(self, app=None, **kwargs):
        self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):

        app._githubhook_ext = self

        app._githubhooks = []
        def githubhook(func):
            app._githubhooks.append(func)
        app.githubhook = githubhook

        app.register_blueprint(blueprint, **kwargs)

        app.config.setdefault('GITHUB_ALLOWED_OWNERS', None)
        app.config.setdefault('GITHUB_CLONE_DIR', os.path.join(app.instance_path, 'repos'))

    def assert_remote_netmask(self):
        if not current_app.debug and not utils.addr_in_network(request.remote_addr, self.remote_netmask):
            log.warning('not from GitHub')
            return 'remote address is not from GitHub'



