import os
from urlparse import parse_qsl

import requests

from . import *


@app.route('/login')
def login():
    if 'access_token' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))


@app.route('/not_authorized')
def not_authorized():
    return render_template('not_authorized.html')


@app.route('/github/login')
def github_login():
    return redirect(
        'https://github.com/login/oauth/authorize?' +
        '&'.join('%s=%s' % (k, v) for k, v in [
            ('client_id', app.config['GITHUB_CLIENT_ID']),
            ('redirect_uri', request.host_url.rstrip('/') + url_for('github_callback')),
            ('scope', 'repo'),
            ('state', os.urandom(8).encode('hex')),
        ]))


@app.route('/github/callback')
def github_callback():

    code = request.args.get('code')
    if not code:
        return redirect(url_for('index'))

    res = requests.post('https://github.com/login/oauth/access_token', data={
        'client_id': app.config['GITHUB_CLIENT_ID'],
        'client_secret': app.config['GITHUB_CLIENT_SECRET'],
        'code': code,
    })

    res_data = dict(parse_qsl(res.text))
    access_token = res_data.get('access_token')
    if access_token:
        session['access_token'] = access_token

    return redirect(url_for('index'))

