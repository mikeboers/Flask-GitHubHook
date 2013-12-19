from setuptools import setup, find_packages

setup(
    
    name='Flask-GitHubHook',
    version='0.1.0',
    description='Tools and small app reacting to GitHub webhooks.',
    url='http://github.com/mikeboers/Flask-GitHubHook',
    
    packages=find_packages(),
    
    author='Mike Boers',
    author_email='githubhook@mikeboers.com',
    license='BSD-3',

    install_requires='''
        Flask>=0.10.1
        Flask-Mako>=0.3
    ''',

)
