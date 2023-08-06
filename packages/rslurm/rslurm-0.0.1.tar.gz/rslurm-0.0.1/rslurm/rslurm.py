import collections
import os
import subprocess

from fabric import Connection


def upload(config):
    exclude = config.exclude
    if isinstance(exclude, collections.Mapping):
        exclude = exclude.get('local', [])
    remote_path = os.path.abspath(os.path.join(config.remote_path, '..'))
    cmd = ['rsync', '-a', config.local_path, ' {}:{}'.format(config.remote_uri, remote_path),
           '--exclude'] + exclude
    print(cmd)
    subprocess.call(cmd)


def download(config):
    exclude = config.exclude
    if isinstance(exclude, collections.Mapping):
        exclude = exclude.get('remote', [])
    remote_path = os.path.abspath(os.path.join(config.remote_path, '..'))
    cmd = ['rsync', '-a', '{}:{}'.format(config.remote_uri, remote_path), config.local_path,
           '--exclude'] + exclude
    subprocess.call(cmd)


def list(config):
    conn = Connection(config.remote_uri)
    with conn.cd(config.remote_path):
        result = conn.run('ls', hide=True)
        print(result.stdout.strip())
    return None


def delete(config):
    conn = Connection(config.remote_uri)
    if input('You are trying to delete \'{}\'. Are you sure? '.format(config.remote_path)).lower() == 'yes':
        result = conn.run('rm -rf {}'.format(config.remote_path), hide=True)
        print(result.stdout.strip())
    return None
