Flask-GitHubHook
================

A Flask blueprint for recieving GitHub post-recieve webhooks, and a small Flask app for running shell scripts.


Installation
------------

1. Create a user on GitHub for doing backups.
2. Add this user (read-only) to any repos/organizations.
3. Setup an SSH key for the user under which this will run, and add it to the GitHub account.
4. Install the code:

~~~bash
git clone git@github.com:mikeboers/Flask-GitHubHook.git
cd Flask-GitHubHook
. bin/bootstrap.sh
~~~

5. Add the hook (`http://dev1.fluentimage.com:8010/`) to every you want to back up.


### Running in Development

~~~
DEBUG=1 python -m githubhookapp
# or
honcho start
~~~

Send the example payload:

~~~
curl -d "payload=$(cat example-payload.json)" http://localhost:5000/hook
~~~


### Running in Production

~~~
honcho export --app githubhook --port 8000 --log var/log upstart var/upstart
sudo cp var/upstart/* /etc/init/
sudo start githubhook
~~~

