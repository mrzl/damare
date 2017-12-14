import os


class Local(object):
    def __init__(self):
        self.images_folder = '/home/mar/code/marcel/damare/data/style_images/'

    def style_images(self):
        return [f for f in os.listdir(self.images_folder) if os.path.isfile(os.path.join(self.images_folder, f))]
