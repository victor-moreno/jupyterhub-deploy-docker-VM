import os
import shutil
import yaml
import uuid

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='openvscode', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_openvscode(prog):
    if shutil.which(prog):
        return prog
    raise FileNotFoundError(f'Could not find {prog} in PATH')

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'openvscode.svg'
    )

def setup_openvscode():
  def _get_cmd(port):
    cmd = [
            get_openvscode('server.sh'), 
            '--port={port}',
            '--without-connection-token',
            '--accept-server-license-terms',
            '--use-host-proxy',
            '--disable-telemetry=true'

    ]
    return cmd
  
  return {
    'command': _get_cmd,
    'timeout': 20,
    'new_browser_tab': get_key('new_browser'),
    'launcher_entry': {
      'title': 'OpenVSCode Server',
      'icon_path': get_icon_path()
    }
  }
