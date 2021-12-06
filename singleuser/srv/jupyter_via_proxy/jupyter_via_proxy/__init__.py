import os
import yaml

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='via', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_icon_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'via.svg')
    
def setup_via():
    def _get_cmd(port):
        cmd = [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'via'), 
                '--base={base_url}via', 
                '--listen=127.0.0.1', 
                '--port={port}'
              ]
        return cmd
    return {
          'command': _get_cmd,
          'timeout': 180,
          'new_browser_tab': get_key('new_browser'),
          'launcher_entry': {
              'title': 'VGG Image Annotator',
              'icon_path': get_icon_path()
          }
    }