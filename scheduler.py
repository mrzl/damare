from os import listdir, remove, rename, makedirs
from os.path import isfile, join, isdir, getmtime
import sys
import time
import subprocess


class Scheduler(object):
    """
    a bash file scheduler in python3

    it makes sure that only one job is running at a time

    should be added as a cronjob (crontab -e)
    (* * * * * python3 /opt/scheduler/scheduler.py >> /opt/scheduler/cron.log)

    jobs are bash files in /opt/scheduler/jobs/
    they'll will be run according to the modification date of the file
    make sure they are executable (chmod a+x job.sh)

    done/failed jobs will be moved to a done/failed subfolder
    """
    def __init__(self):
        self.continue_on_fail = True
        self._jobs_path = '/opt/scheduler/jobs/'
        #self._jobs_path = '/home/mar/jobs/'
        self._log_file = join(self._jobs_path, 'log.txt')
        self._lock_file = join(self._jobs_path, 'lock.lck')
        self._finished_path = join(self._jobs_path, 'done')
        self._failed_path = join(self._jobs_path, 'failed')

        if not isdir(self._jobs_path):
            makedirs(self._jobs_path)
        if not isdir(self._finished_path):
            makedirs(self._finished_path)
        if not isdir(self._failed_path):
            makedirs(self._failed_path)

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
            dst += str(int(time.time()))
        rename(src, dst)

    def run(self):
        script = self.scripts[0][0]
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
                # unlock and move job to failed
                if self.continue_on_fail:
                    self.unlock()
                    self.move_job(script_to_run, self._failed_path, script)

        except OSError as e:
            print("OS error in run(): {0}".format(e))
            self.cleanup()

    @staticmethod
    def cleanup():
        sys.exit(1)

    def sort(self, file_names):
        sort_me = {}
        for filename in file_names:
            sort_me[filename] = getmtime(join(self._jobs_path, filename))

        sorted_scripts = [(k, sort_me[k]) for k in sorted(sort_me, key=sort_me.get, reverse=False)]
        return sorted_scripts

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
