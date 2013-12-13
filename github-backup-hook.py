import errno
import json
import os
from subprocess import check_output

from flask import Flask, request


app = Flask(__name__)
@app.route('/', methods=['POST'])
def main():

    payload = json.loads(request.form['payload'])
    owner_name = payload['repository']['owner']['name']
    repo_name = payload['repository']['name']

    local_path = os.path.abspath(os.path.join(
        __file__, '..', 'repositories', owner_name, repo_name + '.git'
    ))
    remote_url = 'git@github.com:%s/%s.git' % (owner_name, repo_name)

    if not os.path.exists(local_path):
        os.makedirs(local_path)
        return check_output(['git', 'clone', '--bare', remote_url, local_path])
    else:
        return check_output(['git', '--git-dir', local_path, 'fetch', remote_url])


app.run(debug=bool(os.environ.get('DEBUG')), port=int(os.environ.get('PORT', 5000)))

