import setuptools

setuptools.setup(
  name="jupyter_openrefine_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_openrefine_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy openrefine",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],

  entry_points={
      'jupyter_serverproxy_servers': [ 
        'openrefine = jupyter_openrefine_proxy:setup_openrefine' 
      ]
  },
  package_data={ 
      'jupyter_openrefine_proxy': ['icons/openrefine.svg']
  },

  install_requires=['jupyter-server-proxy', 'pyyaml'],
)
