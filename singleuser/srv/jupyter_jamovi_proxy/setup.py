import setuptools

setuptools.setup(
  name="jupyter_jamovi_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_jamovi_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy code-server",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],

  entry_points={
      'jupyter_serverproxy_servers': [
          # name = packagename:function_name
          'jamovi = jupyter_jamovi_proxy:setup_jamovi',
      ]
  },
  package_data={
      'jupyter_jamovi_proxy': ['icons/jamovi.svg'],
  },

  install_requires=['jupyter-server-proxy','pyyaml'],
)

# requires: https://github.com/jamovi/jamovi
