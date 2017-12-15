from fabric_helper import FabricHelper

import os


class Lyrik(object):
    def __init__(self):
        self.fabric = FabricHelper()

        self.style_model_folder = '/home/marcel/drive/marcel/damare/0_FAST_NEURAL_STYLE_MODELS/'
        self.style_images_folder = '/home/marcel/drive/marcel/damare/1_FAST_NEURAL_STYLE_IMAGES/'
        self.content_videos_folder = '/home/marcel/drive/marcel/damare/2_CONTENT_VIDEOS/'
        self.finished_videos_folder = '/home/marcel/drive/marcel/damare/3_FINISHED/'

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