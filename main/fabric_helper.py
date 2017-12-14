import configparser
from fabric.api import run, cd, env, put
from fabric.network import disconnect_all


class FabricHelper(object):
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('settings.ini')

        self._host = cfg.get('lyrik', 'host')
        self._key = cfg.get('lyrik', 'key')
        self._home_dir = cfg.get('lyrik', 'home_dir')
        self._password = cfg.get('lyrik', 'password')

        env.host_string = self._host
        env.key_filename = self._key
        env.password = self._password
        #with cd(self._home_dir):

    def upload(self, origin, destination):
        put(origin, destination, use_sudo=False, mirror_local_mode=True)

    def uname(self):
        return run("uname -a")

    def python_v(self):
        return run("python -V")

    def pip_v(self):
        return run("pip -V")

    def ls(self, dir):
        """
        returns a list of absolute paths of files in the dir
        """
        string = run("for i in %s*; do echo $i; done" % dir)
        return string.replace("\r", "").split("\n")

    def disconnect(self):
        disconnect_all()