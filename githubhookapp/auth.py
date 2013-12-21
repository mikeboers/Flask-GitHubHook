from githubhookapp.core import app
from githubhookapp.github import api


@app.context_processor
def auth_context():
    user_info = api('user') or {}
    return {
        'user_info': user_info,
        'user_login': user_info.get('login'),
    }

