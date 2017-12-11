from os import listdir, remove, rename
from os.path import isfile, join
import sys
import time
import subprocess


class Scheduler(object):
    """
    job files have the following convention
    job_1355563265.sh (job_ + time.time() + .sh)
    """
    def __init__(self):
        #self._path = '/home/marcel/jobs/'
        self._jobs_path = '/home/mar/jobs/'
        self._log_file = join(self._jobs_path, 'log.txt')
        self._lock_file = join(self._jobs_path, 'lock.lck')
        self._finished_path = join(self._jobs_path, 'done')
        self.sorted_scripts = []

        if self.is_locked():
            print('locked: still running')
            sys.exit(0)

        try:
            files = [f for f in listdir(self._jobs_path) if isfile(join(self._jobs_path, f))]
            self.scripts = [x for x in files if x.endswith('.sh')]

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

    def run(self):
        script = self.scripts[0]
        script_to_run = join(self._jobs_path, script)

        try:
            self.lock()
            success = subprocess.call([script_to_run])
            with open(self._log_file, 'a') as f:
                iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
                f.write(iso_time + ': ' + script_to_run + ' with return ' + str(success) + '\n')

            if success is 0:
                self.unlock()
                rename(script_to_run, join(self._finished_path, script))

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
