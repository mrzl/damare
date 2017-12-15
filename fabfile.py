from fabric.api import *

env.hosts = ['marcel@lyrik.ddns.net']
env.key_filename = '/home/mar/.ssh/id_rsa_marchi'
env.password = open('pass', 'r').readlines()[0]


def hello(name="hoho"):
    print("hey " + name)


def uname():
    local("uname -a")


def deploy():
    home_dir = "/home/marcel/fabric"
    with cd(home_dir):
        run("uname -a")

        run("python -V")
        run("pip -V")


def deploy_scheduler():
    send('/home/mar/code/marcel/lyrik/scheduler/scheduler.py', '/opt/scheduler/')


def deploy_scripts():
    send('/home/mar/code/marcel/damare/scripts/train_r01.sh', '/opt/scheduler/jobs/')
    send('/home/mar/code/marcel/damare/scripts/train_r02.sh', '/opt/scheduler/jobs/')
    send('/home/mar/code/marcel/damare/scripts/train_r03.sh', '/opt/scheduler/jobs/')


def send(local_path, remote_path):
    put(local_path, remote_path, use_sudo=False, mirror_local_mode=True)


def dl(remote_path, local_path):
    get(remote_path, local_path)