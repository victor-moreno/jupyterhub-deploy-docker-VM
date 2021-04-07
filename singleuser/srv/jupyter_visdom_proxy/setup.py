import setuptools

setuptools.setup(
  name="jupyter_visdom_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_visdom_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy visdom",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],

  entry_points={
      'jupyter_serverproxy_servers': [
          'visdom = jupyter_visdom_proxy:setup_visdom',
      ]
  },
  install_requires=['jupyter-server-proxy','visdom','pyyaml'],
)

# requires: conda install -c conda-forge code-server
# code-server in PATH