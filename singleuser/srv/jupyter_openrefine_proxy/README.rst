jupyter openrefine proxy

Adds a proxy service to jupyter to work with openrefine

config file:
    ~/.jupyter/services.yaml
    
    - openrefine:
        new_browser: True  # open as new tab in browser
        memory: 4096M
        data_dir: ~/.local/share/openrefine/

