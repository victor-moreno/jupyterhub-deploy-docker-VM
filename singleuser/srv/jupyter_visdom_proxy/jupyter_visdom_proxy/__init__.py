import os
import shutil
import yaml

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='visdom', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_visdom(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def setup_visdom():
  def _get_cmd(port):
    cmd = [
            get_visdom('visdom'),
            '--hostname=0.0.0.0',
            '-port={port}',
            '-proxy_url={base_url}visdom',
    ]
    return cmd
  
  return {
    'command': _get_cmd,
    'timeout': 20,
    'new_browser_tab': get_key('new_browser'),
    'launcher_entry': {
      'title': 'Visdom',
    }
  }
