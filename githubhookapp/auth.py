from githubhookapp.core import app
from githubhookapp.github import get_user_info


@app.context_processor
def auth_context():
    user_info = get_user_info() or {}
    return {
        'user_info': user_info,
        'user_login': user_info.get('login'),
    }

