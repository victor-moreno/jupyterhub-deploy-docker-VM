import os
import yaml

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='deepzoom', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_images_dir():
    images_dir = get_key('images_dir')
    if images_dir == None:
        images_dir =  os.path.expanduser('~/images')
    if not os.path.isdir(images_dir):
        os.mkdir(images_dir)
        if not os.path.isdir(images_dir):
            raise Exception(f'Could not create {images_dir}')
    return images_dir            

def get_image_folder():
    filename = os.path.expanduser('~/.images')
    if os.path.isfile(filename):
        with open(filename) as f:
            image_folder = f.readline().rstrip()

    if not image_folder or image_folder == "":
        home_images = os.path.isdir('/home/jovyan/images')
        if os.path.isdir(home_images):
            image_folder = '/home/jovyan/images'
        else:
            image_folder = '/home/jovyan'

    return image_folder

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'deepzoom.svg'
    )

def get_new_browser():
    # if file ~/.jupyter/.new_browser exists, open in new browser
    return os.path.isfile(os.path.expanduser('~/.jupyter/.new_browser'))

def get_deepzoom_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'deepzoom_multiserver'
    )

def setup_deepzoom():
    def _get_cmd(port):
        cmd = [
                get_deepzoom_path(), 
                '--base={base_url}deepzoom', 
                '--listen=127.0.0.1', 
                '--port={port}',
                get_image_folder()
              ]
        return cmd
    return {
          'command': _get_cmd,
          'timeout': 120,
          'new_browser_tab': get_key('new_browser'),
          'launcher_entry': {
              'title': 'Deepzoom openslide',
              'icon_path': get_icon_path()
          }
    }