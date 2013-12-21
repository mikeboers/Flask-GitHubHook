from . import *


@app.route('/')
def index():
    return render_template('index.html',
        user_orgs=github_api('user/orgs'),
    )
