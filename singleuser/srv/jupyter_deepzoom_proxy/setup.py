import setuptools

setuptools.setup(
  name="jupyter_deepzoom_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_deepzoom_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy openslide deepzoom",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],
  entry_points={
      'jupyter_serverproxy_servers': [ 'deepzoom = jupyter_deepzoom_proxy:setup_deepzoom' ],
  },
  package_data={ 
      'jupyter_deepzoom_proxy': [ 'deepzoom_multiserver', 'icons/deepzoom.svg', 'templates/*.html', 'static/*.js', 'static/images/*.png' ]
  }, 
  include_package_data=True,
  install_requires=['jupyter-server-proxy', 'flask','openslide-python','pyyaml'],
)

# requires: conda install -c conda-forge openslide flask
#           pip install openslide-python
