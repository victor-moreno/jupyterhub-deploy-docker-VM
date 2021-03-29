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
        os.makedirs(images_dir, exist_ok=True)
        if not os.path.isdir(images_dir):
            raise Exception(f'Could not create {images_dir}')
    return images_dir            

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'deepzoom.svg'
    )

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
                get_images_dir()
              ]
        return cmd
    return {
          'command': _get_cmd,
          'timeout': 180,
          'new_browser_tab': get_key('new_browser'),
          'launcher_entry': {
              'title': 'Deepzoom openslide',
              'icon_path': get_icon_path()
          }
    }