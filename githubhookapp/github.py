import json

import requests
from flask import session

from githubhookapp.core import app, memo


def get_user_info():
    return _get_user_info(session.get('access_token'))

@memo
def _get_user_info(access_token):
    return json.loads(requests.get('https://api.github.com/user', params={
        'access_token': access_token,
    }).text)


def get_user_orgs():
    return _get_user_orgs(session.get('access_token'))

@memo
def _get_user_orgs(access_token):
    return json.loads(requests.get('https://api.github.com/user/orgs', params={
        'access_token': access_token,
    }).text)

