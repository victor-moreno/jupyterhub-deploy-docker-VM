import setuptools

setuptools.setup(
  name="jupyter_via_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_via_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy VGG Image Annotator (VIA)",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],
  entry_points={
      'jupyter_serverproxy_servers': [ 'via = jupyter_via_proxy:setup_via' ],
  },
  package_data={ 
      'jupyter_via_proxy': [ 'via', 'icons/via.svg', 'templates/via.html' ]
  }, 
  include_package_data=True,
  install_requires=['jupyter-server-proxy', 'flask', 'pyyaml'],
)

# requires: conda install -c conda-forge openslide flask
