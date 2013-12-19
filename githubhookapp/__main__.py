import os

from githubhookapp.webapp import app

app.run(port=int(os.environ.get('PORT', 5000)))

