c.NotebookApp.default_url = '/lab'

c.ServerProxy.servers = {
  'code-server': {
    'command': [
      'code-server',
        '--auth=none',
        '--disable-telemetry',
        '--bind-addr=localhost:{port}'
    ],
    'timeout': 20,
    'launcher_entry': {
      'title': 'VS Code'
    }
  },
  'rstudio': {
    'command': [
      '/usr/lib/rstudio-server/bin/rserver',
      '--config-file=/home/jovyan/.jupyter/rstudio.conf',
      '--www-port={port}'
    ],
    'timeout': 20,
    'launcher_entry': {
      'title': 'RStudio'
    },
    'new_browser_tab': True
  }
}
