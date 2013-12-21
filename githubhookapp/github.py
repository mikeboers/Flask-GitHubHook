import json

import requests
from flask import session

from githubhookapp.core import app, memo


def api(method, **params):
    access_token = session.get('access_token')
    if access_token:
        return _api(method, access_token=access_token, **params)


@memo
def _api(method, **params):
    method = method.format(**params)
    return requests.get(
        'https://api.github.com/' + method.strip('/'),
        params=params,
    ).json()

