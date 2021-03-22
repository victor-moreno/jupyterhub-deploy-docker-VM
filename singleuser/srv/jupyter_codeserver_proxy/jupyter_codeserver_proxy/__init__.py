import os
import shutil
import yaml

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='codeserver', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_codeserver(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'codeserver.svg'
    )

def get_new_browser():
    # if file ~/.jupyter/.new_browser exists, open in new browser
    return os.path.isfile(os.path.expanduser('~/.jupyter/.new_browser'))


def setup_codeserver():
  def _get_cmd(port):
    cmd = [
            get_codeserver('code-server'), 
            '--auth=none', 
            '--disable-telemetry', 
            '--bind-addr=127.0.0.1:{port}'
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
