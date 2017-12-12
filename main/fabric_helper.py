import configparser
from fabric.api import run, cd, env, execute
from fabric.network import disconnect_all
from fabric.context_managers import settings, hide


class FabricHelper(object):
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read("settings.ini")

        self._host = cfg.get("lyrik", "host")
        self._key = cfg.get("lyrik", "key")
        self._home_dir = cfg.get("lyrik", "home_dir")
        self._password = cfg.get("lyrik", "password")

        env.host_string = self._host
        env.key_filename = self._key
        env.password = self._password
        #with cd(self._home_dir):

    def uname(self):
        return run("uname -a")

    def python_v(self):
        return run("python -V")

    def pip_v(self):
        return run("pip -V")

    def disconnect(self):
        disconnect_all()

    def capture(self):
        with settings(hide('running', 'commands', 'stdout', 'stderr')):
            stdout = execute(self.uname, hosts=self._host)
        return stdout
