from os.path import join

from fabric.operations import run, local
from fabric.api import task
from fabric.state import env
from contextlib import contextmanager
from fabric.api import *


env.user = 'root'
env.http_user = 'www-data'
env.http_group = 'www-data'
env.hosts = ['104.236.42.196']
env.www_path = '/var/www'
env.path = join(env.www_path, 'astrology')
env.app_path = join(env.path, 'astro')
env.server_conf = 'astro/config/apache2/astro.conf'

env.venv_name = 'venv'
env.venv_path = join(env.www_path, env.venv_name)
env.github_repo = 'git@github.com:flp9001/astrology.git'
env.activate = 'source {venv_path}/bin/activate'.format(**env)


@contextmanager
def virtualenv():
    with cd(env.path):
        with prefix(env.activate):
            yield

@task
def os_dep():
    with cd(env.path):
        run('./install_os_dependencies.sh install')

@task 
def py_dep():
    with virtualenv():
        run("pip install -r {path}/requirements/production.txt".format(**env))

@task
def restart():
    with cd(env.path):
        run('cp {server_conf} /etc/apache2/sites-enabled/'.format(**env))
    run('service apache2 restart')


@task
def initial_setup():
    run('mkdir -p {www_path}'.format(**env))
    with cd(env.www_path):
        run('git clone {github_repo}'.format(**env))
        run('virtualenv {venv_name}'.format(**env))    
    os_dep()
    py_dep()
    
    


@task
def deploy():
    local('git push --all')
    with cd(env.path):
        run("git reset --hard")
        run("git pull")
        run("git checkout -f")
        run("chown -R {http_user}:{http_group} .".format(**env))
    os_dep()
    py_dep()
    with virtualenv():
        with cd(env.app_path):
            with shell_env(DJANGO_SETTINGS_MODULE='config.settings.production'):
                run('python manage.py migrate')
        
    restart()

@task
def test():
    with virtualenv():
        with cd(env.app_path):
            run('echo $DJANGO_SETTINGS_MODULE')
