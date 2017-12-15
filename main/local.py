import os


class Local(object):
    def __init__(self):
        self.images_folder = '/home/mar/code/marcel/damare/data/style_images/'
        self.video_folder = '/home/mar/code/marcel/damare/data/content/'

    def style_images(self):
        return [f for f in os.listdir(self.images_folder) if os.path.isfile(os.path.join(self.images_folder, f))]

    def content_videos(self):
        return [f for f in os.listdir(self.video_folder) if os.path.isfile(os.path.join(self.video_folder, f))]