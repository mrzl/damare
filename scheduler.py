from os import listdir, remove, rename, makedirs
from os.path import isfile, join, isdir
import sys
import time
import subprocess


class Scheduler(object):
    """
    python3 'cause of subprocess.run

    job files have the following convention
    job_1355563265.sh (job_ + time.time() + .sh)
    """
    def __init__(self):
        self.continue_on_fail = True
        self._jobs_path = '/opt/scheduler/jobs/'
        #self._jobs_path = '/home/mar/jobs/'
        self._log_file = join(self._jobs_path, 'log.txt')
        self._lock_file = join(self._jobs_path, 'lock.lck')
        self._finished_path = join(self._jobs_path, 'done')
        self._failed_path = join(self._jobs_path, 'failed')
        self.sorted_scripts = []

        if self.is_locked():
            print('locked: still running')
            sys.exit(0)

        try:
            files = [f for f in listdir(self._jobs_path) if isfile(join(self._jobs_path, f))]
            self.scripts = [x for x in files if x.endswith('.sh') and 'job_' in x]
            self.scripts = self.sort(self.scripts)

            # no scripts found, abort
            if len(self.scripts) is 0:
                self.cleanup()

        except OSError as e:
            print("OS error: {0}".format(e))
            self.cleanup()

    def is_locked(self):
        return isfile(self._lock_file)

    def lock(self):
        print('locking')
        open(self._lock_file, 'w').close()

    def unlock(self):
        print('unlocking')
        remove(self._lock_file)

    def move_job(self, src, dstdir, dstfile):
        if not isdir(dstdir):
            makedirs(dstdir)
        dst = join(dstdir, dstfile)
        if isfile(dst):
            # if destination file already exists,
            # append current timestamp in order to not overwrite
            dst += str(time.time())
        rename(src, dst)

    def run(self):
        script = self.scripts[0]
        script_to_run = join(self._jobs_path, script)

        try:
            self.lock()
            with open(self._log_file, 'a') as f:
                iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
                f.write(iso_time + ': ' + script_to_run + ' started\n')
            success = subprocess.run([script_to_run])
            with open(self._log_file, 'a') as f:
                iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
                f.write(iso_time + ': ' + str(success) + '\n')

            if success.returncode is 0:
                self.unlock()
                self.move_job(script_to_run, self._finished_path, script)
            else:
                # unlock and
                if self.continue_on_fail:
                    self.unlock()
                    self.move_job(script_to_run, self._failed_path, script)

        except OSError as e:
            print("OS error in run(): {0}".format(e))
            self.cleanup()

    @staticmethod
    def cleanup():
        # remove lock file
        sys.exit(1)

    @staticmethod
    def sort(file_names):
        to_sort = []

        for filename in file_names:
            try:
                tmp = filename[4:]
                tmp = tmp[:-3]
                utc = int(tmp)
                to_sort.append(utc)
            except ValueError as e:
                print("ValueError: {0}".format(e))

        to_sort.sort()
        sorted_scripts = []

        for s in to_sort:
            sorted_scripts.append('job_' + str(s) + '.sh')

        return sorted_scripts

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
