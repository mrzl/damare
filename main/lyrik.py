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
        self._fast_artistic_style_folder = '/home/marcel/devel/fast-artistic-videos/'
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
            if f.endswith('.jpg') or f.endswith('.png') or self.fabric.ERROR in f:
                path, file = os.path.split(f)
                only_images.append(file)

        return only_images

    def content_videos(self):
        file_list = self.fabric.ls(self.content_videos_folder)
        only_videos = []
        for f in file_list:
            if f.endswith('.mp4') or f.endswith('.mov') or self.fabric.ERROR in f:
                path, file = os.path.split(f)
                only_videos.append(file)

        return only_videos

    def train(self, style_image, style_size, content_weight, style_weight):
        style = style_image[:-4]
        style_job_filename = 'train_' + style + '.sh'
        style_job_path = os.path.join(self.scheduler_jobs_folder, style_job_filename)
        self.fabric.touch(style_job_path)
        self.fabric.echo(style_job_path, '#!/bin/sh\nsource /home/marcel/.bashrc\n\ncd '
                                         '~/devel/fast-neural-style/\n/mnt/drive1/tools/torch2/install/bin/th '
                                         'train.lua -h5_file '+self.style_model_folder +
                                         'new_trained_output_all_coco.h5 -style_image ' + self.style_images_folder
                         + style_image+' -style_image_size ' + style_size+' -content_weights '
                         + content_weight+' -style_weights ' + style_weight+' -checkpoint_name ' + style+' -gpu 0\n'
                         + 'mv '+style+'* ' + self.style_model_folder)
        self.fabric.chmod(style_job_path, 'a+x')

    def render(self, content_video, style_file, resolution, do_waifu, fps):
        style = style_file[:-3]
        video = content_video[:-4]

        render_job_filename = 'render_' + style + '_' + video + '_' + fps

        www = ''

        if do_waifu:
            www += '_waifued'

        render_job_filename += www
        render_job_filename += '.sh'

        resolution_split = resolution.split(':')

        render_job_path = os.path.join(self.scheduler_jobs_folder, render_job_filename)
        self.fabric.touch(render_job_path)
        self.fabric.echo(render_job_path, '#!/bin/bash\nsource /home/marcel/.bashrc\n\ncd' + self._fast_artistic_style_folder + '\nbash fast_stylize.sh '+self.content_videos_folder+content_video+' ' +self.style_model_folder+style_file+'\nbash opt_flow.sh '+video+'/frame_%06d.ppm '+video+'/flow_'+resolution_split[0]+'\\:'+resolution_split[1]+'/\nbash make_video.sh '+self.content_videos_folder+content_video+'\n\ncd /home/marcel/devel/waifu2x/\nfind '+self._fast_artistic_style_folder+video+'/ -name "out-*.png" | sort > image_list_temp.txt\nmkdir '+self._fast_artistic_style_folder+video+'/high\n\n/mnt/drive1/tools/torch2/install/bin/th waifu2x.lua -m noise_scale -noise_level 3 -force_cudnn 1 -l ./image_list_temp.txt -o '+self._fast_artistic_style_folder+video+'/high/out_high_%06d.png\n\n/usr/bin/ffmpeg -y -framerate '+fps + ' -i '+self._fast_artistic_style_folder+'/high/out_high_%06d.png '+self.finished_videos_folder+style+'_'+video+www+'_'+fps+'.mp4\n\nrm -r '+self._fast_artistic_style_folder+video+'\nrm -r '+self._fast_artistic_style_folder+video+'_1\nrm '+self._fast_artistic_style_folder+video+'-stylized.mp4\n')
        self.fabric.chmod(render_job_path, 'a+x')

    def upload(self, destination_dir, files):
        for file in files:
            self.fabric.upload(file, destination_dir)

    def uname(self):
        return self.fabric.uname()

    def python_version(self):
        return self.fabric.python_v()

    def pip_version(self):
        return self.fabric.pip_v()

    def disconnect(self):
        self.fabric.disconnect()