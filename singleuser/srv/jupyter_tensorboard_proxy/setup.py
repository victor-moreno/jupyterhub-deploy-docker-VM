import setuptools

setuptools.setup(
  name="jupyter_tensorboard_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_tensorboard_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy tensorboard",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],

  entry_points={
      'jupyter_serverproxy_servers': [
          'tensorboard = jupyter_tensorboard_proxy:setup_tensorboard',
      ]
  },
  package_data={
      'jupyter_tensorboard_proxy': ['icons/tensorboard.svg'],
  },
  install_requires=['jupyter-server-proxy','tensorboard','pyyaml'],
)

# requires: conda install -c conda-forge code-server
# code-server in PATH