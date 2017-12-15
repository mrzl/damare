from fabric_helper import FabricHelper
import configparser

import os


class Lyrik(object):
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('settings.ini')
        self.host = cfg.get('lyrik', 'host')
        self.key = cfg.get('lyrik', 'key')
        self.password = cfg.get('lyrik', 'password')

        self.fabric = FabricHelper(self.host, self.key, self.password)

        self.style_model_folder = '/home/marcel/drive/marcel/damare/0_FAST_NEURAL_STYLE_MODELS/'
        self.style_images_folder = '/home/marcel/drive/marcel/damare/1_FAST_NEURAL_STYLE_IMAGES/'
        self.content_videos_folder = '/home/marcel/drive/marcel/damare/2_CONTENT_VIDEOS/'
        self.finished_videos_folder = '/home/marcel/drive/marcel/damare/3_FINISHED/'
        self.scheduler_jobs_folder = '/opt/scheduler/jobs/'

    def models(self):
        file_list = self.fabric.ls(self.style_model_folder)
        only_t7_files = []
        for f in file_list:
            if f.endswith('.t7') or self.fabric.ERROR in f:
                path, file = os.path.split(f)
                only_t7_files.append(file)

        return only_t7_files

    def style_images(self):
        file_list = self.fabric.ls(self.style_images_folder)
        only_images = []
        for f in file_list:
            if f.endswith('.jpg') or f.endswith('.png')or self.fabric.ERROR in f:
                path, file = os.path.split(f)
                only_images.append(file)

        return only_images

    def train(self, style_image, style_size, content_weight, style_weight):
        style = style_image[:-4]
        style_job_filename = 'train_' + style + '.sh'
        style_job_path = os.path.join(self.scheduler_jobs_folder, style_job_filename)
        self.fabric.touch(style_job_path)
        self.fabric.echo(style_job_path, '#!/bin/sh\nsource /home/marcel/.bashrc\n\ncd ~/devel/fast-neural-style/\n/mnt/drive1/tools/torch2/install/bin/th train.lua -h5_file '+self.style_model_folder + 'new_trained_output_all_coco.h5 -style_image ' + self.style_images_folder + style_image+' -style_image_size ' + style_size+' -content_weights ' + content_weight+' -style_weights ' + style_weight+' -checkpoint_name ' + style+' -gpu 0\n')
        self.fabric.chmod(style_job_path, 'a+x')

    async def upload(self, destination_dir, files):
        for file in files:
            await self.fabric.upload(file, destination_dir)

    def uname(self):
        return self.fabric.uname()

    def python_version(self):
        return self.fabric.python_v()

    def pip_version(self):
        return self.fabric.pip_v()

    def disconnect(self):
        self.fabric.disconnect()