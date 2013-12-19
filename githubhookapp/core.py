import atexit
import copy
import errno
import os
import threading
from subprocess import Popen, PIPE
from Queue import Queue

from flask import Flask
from flask.ext.githubhook import GitHubHook

app = Flask(__name__)
app.root_path = os.path.abspath(os.path.join(__file__, '..', '..'))
app.instance_path = os.path.join(app.root_path, 'var')

app.config['GITHUB_ALLOWED_OWNERS'] = set(['mikeboers', 'FluentImage'])
app.debug = app.debug or bool(os.environ.get('DEBUG'))

githubhook = GitHubHook(app=app, url_prefix='/hook')


hook_queue = Queue()

def worker():
    while True:

        job = hook_queue.get()
        if job is None:
            return

        try:
            call_hook(*job)
        finally:
            hook_queue.task_done()

worker_thread = threading.Thread(target=worker)
worker_thread.daemon = True
worker_thread.start()

@atexit.register
def worker_cleanup():
    hook_queue.put(None)
    if worker_thread:
        worker_thread.join()


@app.githubhook
def schedule_hooks(payload):

    hooks = []
    for path in (
        os.path.join(app.root_path, 'etc', 'hooks'),
        os.path.join(app.instance_path, 'etc', 'hooks'),
    ):
        try:
            hooks.extend(os.path.join(path, x) for x in os.listdir(path))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    payload = copy.deepcopy(payload)

    for hook in sorted(hooks, key=os.path.basename):
        if hook.endswith('.example'):
            continue
        hook_queue.put((hook, payload))


def call_hook(hook, payload):

    env = os.environ.copy()
    for k, v in app.config.iteritems():
        env.setdefault('FLASK_' + k, str(v))
    
    owner_name = payload['repository']['owner']['name']
    repo_name = payload['repository']['name']

    env['GITHUB_OWNER'] = owner_name
    env['GITHUB_REPO_NAME'] = repo_name
    env['GITHUB_NAME'] = '%s/%s' % (owner_name, repo_name)

    clone_dir = app.config['GITHUB_CLONE_DIR']
    if clone_dir is not None:
        local_path = os.path.join(clone_dir, owner_name, repo_name + '.git')
        env['GITHUB_CLONE'] = local_path

    sandbox = os.path.join(app.instance_path, 'sandbox')
    try:
        os.makedirs(sandbox)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print 'calling', hook
    try:
        if hook.endswith('.sh'):
            proc = Popen(['bash', hook], stdin=PIPE, env=env, cwd=sandbox)
        else:
            proc = Popen([hook], stdin=PIPE, env=env, cwd=sandbox)
    except OSError as e:
        if e.errno != errno.EACCES:
            raise
    else:
        proc.wait()

