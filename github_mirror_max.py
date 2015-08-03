#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import subprocess
asf
# configuration
repos_of = ['maximh-ASG']
backup_dir = os.path.expanduser('~/github') #'Z:\Rye\SCM\Repomirror'

# helpers

class Error(Exception):
    """An error that is not a bug in this script."""

def ensure_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def get_json_and_headers(url):
    with urllib.request.urlopen(url) as r:
        content_type = r.info().get('Content-Type', '').lower()
        if content_type not in ('application/json; charset="utf-8"',
                                'application/json; charset=utf-8'):
            raise Error('Did not get UTF-8 JSON data from {0}, got {1}'
                        .format(url, content_type))
        return json.loads(r.read().decode('UTF-8')), r.info()


def get_github_list(url):
    res, headers = get_json_and_headers('{0}'.format(
        url))
    return res

def info(*args):
    print(" ".join(map(str, args)))
    sys.stdout.flush()

def backup(git_url, dir):
    if os.path.exists(dir):
        subprocess.call(['git', 'fetch'], cwd=dir)
    else:
        subprocess.call(['git', 'clone', '--mirror', git_url])

def update_description(git_dir, description):
    with open(os.path.join(git_dir, 'description'), 'w', encoding='UTF-8') as f:
        f.write(description + '\n')

def update_cloneurl(git_dir, cloneurl):
    with open(os.path.join(git_dir, 'cloneurl'), 'w') as f:
        f.write(cloneurl + '\n')

def back_up_repos_of(username, backup_dir=backup_dir):
    ensure_dir(backup_dir)
    os.chdir(backup_dir)
    for repo in get_github_list('https://api.github.com/users/%s/repos' % username):
        dir = repo['name'] + '.git'
        description = repo['description'] or "(no description)"
        info("+", repo['full_name'])
        backup(repo['clone_url'].replace('github', 'maximh-asg:161ed1cebe05ebadbc699f2323c18feaa2a9d801@github'), dir)
        update_description(dir, description + '\n\n' + repo['html_url'])
        #update_cloneurl(dir, repo['ssh_url'])

# action
if __name__ == '__main__':
    for user in repos_of:
        back_up_repos_of(user)