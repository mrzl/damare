from fabric.api import run, cd, env, put
from fabric.exceptions import NetworkError
from fabric.network import disconnect_all


class FabricHelper(object):
    def __init__(self, host, key, password):
        env.host_string = host
        env.key_filename = key
        env.password = password

        self.ERROR = 'NetworkError'
        #with cd(self._home_dir):

    async def upload(self, origin, destination):
        try:
            await put(origin, destination, use_sudo=False, mirror_local_mode=True)
        except NetworkError as e:
            print(e)

    def uname(self):
        return run("uname -a")

    def python_v(self):
        return run("python -V")

    def pip_v(self):
        return run("pip -V")

    def echo(self, file_path, str):
        return run('echo \"' + str + '\" > ' + file_path)

    def touch(self, file_path):
        return run('touch ' + file_path)

    def chmod(self, file_path, permissions):
        return run('chmod ' + str(permissions) + ' ' + file_path)

    def ls(self, dir):
        """
        returns a list of absolute paths of files in the dir
        """
        try:
            string = run("for i in %s*; do echo $i; done" % dir)
        except NetworkError as e:
            print(e)
            return [self.ERROR]
        return string.replace("\r", "").split("\n")

    def disconnect(self):
        disconnect_all()