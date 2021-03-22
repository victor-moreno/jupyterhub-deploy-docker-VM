jupyter codeserver proxy

Adds a proxy service to jupyterlab to open codeserver

config file:
    ~/.jupyter/services.yaml

    - codeserver:
        new_browser: False  # if True new browser tab is opened
