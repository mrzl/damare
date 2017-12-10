from fabric.api import *

env.hosts = ['marcel@lyrik.ddns.net']
env.key_filename = '/home/mar/.ssh/id_rsa_marchi'


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


def send(local_path, remote_path):
    put(local_path, remote_path, use_sudo=False)