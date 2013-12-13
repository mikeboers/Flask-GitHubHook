import errno
import json
import os
import socket
import struct
from subprocess import call

from flask import Flask, request


ALLOWED_OWNERS = set(['mikeboers', 'FluentImage'])


def ip_to_int(ip):
    "convert decimal dotted quad string to long integer"
    if isinstance(ip, int):
        return ip
    return struct.unpack('!I', socket.inet_aton(ip))[0]

def network_mask(ip, bits):
    "Convert a network address to a long integer" 
    return ip_to_int(ip) & ((2 << bits - 1) - 1)

def addr_in_network(ip, net):
    "Is an address in a network"
    return ip_to_int(ip) & net == net


GITHUB_NETMASK = network_mask('192.30.252.0', 22)


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():

    if not app.debug and not addr_in_network(request.remote_addr, GITHUB_NETMASK):
        return 'You are not GitHub.'

    if request.method != 'POST':
        return 'must POST'

    payload = json.loads(request.form['payload'])
    owner_name = payload['repository']['owner']['name']
    repo_name = payload['repository']['name']

    if owner_name not in ALLOWED_OWNERS:
        return 'owner not permitted'

    local_path = os.path.abspath(os.path.join(
        __file__, '..', 'var', 'repositories', owner_name, repo_name + '.git'
    ))
    remote_url = 'git@github.com:%s/%s.git' % (owner_name, repo_name)

    if not os.path.exists(local_path):
        os.makedirs(local_path)
        call(['git', 'clone', '--mirror', remote_url, local_path])
    else:
        call(['git', '--git-dir', local_path, 'remote', 'set-url', remote_url])
        call(['git', '--git-dir', local_path, 'fetch', 'origin'])

    return 'ok'


app.run(host='', debug=bool(os.environ.get('DEBUG')), port=int(os.environ.get('PORT', 5000)))

