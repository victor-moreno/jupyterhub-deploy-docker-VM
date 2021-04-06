import os
import shutil
import yaml

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='jamovi', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_jamovi(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'jamovi.svg'
    )


def open_jamovi():
    from IPython.display import Javascript
    url = 'http://localhost:41337'
    display(Javascript('window.open("{url}");'.format(url=url)))
      
def setup_jamovi():
  def _get_cmd(port):
    cmd = [
            open_jamovi, 
    ]
    return cmd

  return {
    'command': _get_cmd,
    'timeout': 20,
    'new_browser_tab': get_key('new_browser'),
    'launcher_entry': {
      'title': 'Code Server',
      'icon_path': get_icon_path()
    }
  }
