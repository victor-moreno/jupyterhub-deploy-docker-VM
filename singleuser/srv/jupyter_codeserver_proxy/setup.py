import setuptools

setuptools.setup(
  name="jupyter_codeserver_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_codeserver_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy code-server",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],

  entry_points={
      'jupyter_serverproxy_servers': [
          # name = packagename:function_name
          'codeserver = jupyter_codeserver_proxy:setup_codeserver',
      ]
  },
  package_data={
      'jupyter_codeserver_proxy': ['icons/codeserver.svg'],
  },

  install_requires=['jupyter-server-proxy','pyyaml'],
)

# requires: conda install -c conda-forge code-server
# code-server in PATH