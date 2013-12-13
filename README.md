GitHub Backup Hook
==================

A tiny Flask app for pulling everything pushed to GitHub.


Installation
------------

1. Create a user on GitHub for doing backups.
2. Add this user (read-only) to any repos/organizations.
3. Setup an SSH key for the user under which this will run, and add it to the GitHub account.
4. Install the code:

~~~
git clone git@github.com:FluentImage/github-backup-hook.git
cd github-backup-hook
virtualenv --no-site-packages venv
. venv/bin/activate
pip install flask honcho
honcho export --port 8010 --user dev --log var/log upstart var/upstart
sudo cp var/upstart/* /etc/init/
sudo start github-backup-hook
~~~

