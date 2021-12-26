import os
import shutil
import yaml

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='openrefine', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_data_dir():
    data_dir = get_key('data_dir')
    if data_dir == None:
        data_dir =  os.path.expanduser('~/.local/share/openrefine/')
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        if not os.path.isdir(data_dir):
            raise Exception(f'Could not create {data_dir}')
    return data_dir            

def get_memory():
    memory = get_key('memory')
    if memory == None:
        memory =  '4096M'
    return memory

def get_openrefine(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'openrefine.svg'
    )

def setup_openrefine():
  def _get_cmd(port):
    cmd = [
            get_openrefine('refine'), 
            '-i', '0.0.0.0',
            '-p', '{port}',
            '-m', get_memory(),
            '-d', get_data_dir(),
    ]
    return cmd
  
  return {
    'command': _get_cmd,
    'timeout': 20,
    'new_browser_tab': get_key('new_browser'),
    'launcher_entry': {
      'title': 'Openrefine',
      'icon_path': get_icon_path()
    }
  }
