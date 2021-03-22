jupyter tensorboard proxy

Adds a proxy service to jupyterlab to open tensorboard

config file:
    ~/.jupyter/services.yaml
    
    - tensorboard:
        logdir: /home/jovyan/board  # this is the default. Folder will be created if no exists
        new_browser: True  # open as new tab in browser

