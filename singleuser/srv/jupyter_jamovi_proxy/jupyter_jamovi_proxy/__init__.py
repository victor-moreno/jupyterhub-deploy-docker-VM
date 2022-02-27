import os
import shutil
import yaml
from urllib.parse import urlparse, urlunparse

os.environ["LD_LIBRARY_PATH"]="/usr/local/lib/R/lib"

# load config
with open(os.path.expanduser('~/.jupyter/services.yaml'), 'r') as cfgfile:
    cfg = yaml.load(cfgfile, Loader=yaml.FullLoader)

def get_key(key, app='jamovi', cfg=cfg):
    for a in cfg:
        for k, v in a.items():
            if k == app:
                return v.get(key)

def get_icon_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'icons', 'jamovi.svg'
    )

def rewrite_path(response, request):
    with open("/tmp/rewrite.loc", "a") as f:
        print(f'\n== - ==\n' , file=f)
        q = urlparse(request.uri)
        print(f'path: {q.path}', file = f)
        for header, v in response.headers.get_all():
            print( f"h:\t{header}\t{v}" , file=f)
            if header == "Location":
                # print( f" >\t{urlparse(v)}" , file=f)
                u = urlparse(v)
                u = u._replace(scheme='https')
                u = u._replace(netloc='cuda.odap-ico.org')
                u = u._replace(path=q.path[:-1] + u.path)
                response.headers[header] = urlunparse(u)
                # print( f" <\t{u}" , file=f)
                try:
                  print( f"p\t{p}" , file=f)
                except:
                  print('')
                p = q.path
            # else:
                # u = urlparse(request.uri)
                # response.headers[header] = urlunparse(u._replace(path=u.path+v))

def setup_jamovi():
  def jamovi_cmd(port):
    cmd = [
            "/usr/bin/python3", "-m", "jamovi.server", "{port}", "--if=*"
    ]
    return cmd    

  def dummy_cmd(port):
    cmd = [ "/usr/bin/python3", "-m", "http.server", "{port}" ]
    return cmd    

  with open("/tmp/rewrite.loc", "w") as f:
      print('\n== +++ ==\n' , file=f)
  
  return {
    'command': jamovi_cmd,
    'timeout': 20,
    'new_browser_tab': get_key('new_browser'),
    'rewrite_response': rewrite_path, 
    'launcher_entry': {
      'title': 'Jamovi',
      'icon_path': get_icon_path()
    }
  }
