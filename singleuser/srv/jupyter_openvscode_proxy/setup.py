import setuptools

setuptools.setup(
  name="jupyter_openvscode_proxy",
  version='1.0',
  url="https://github.com/victor-moreno/jupyter_openvscode_proxy",
  author="Victor Moreno",
  description="Jupyter extension to proxy code-server",
  packages=setuptools.find_packages(),
    keywords=['Jupyter'],
    classifiers=['Framework :: Jupyter'],

  entry_points={
      'jupyter_serverproxy_servers': [
          # name = packagename:function_name
          'openvscode = jupyter_openvscode_proxy:setup_openvscode',
      ]
  },
  package_data={
      'jupyter_openvscode_proxy': ['icons/openvscode.svg'],
  },

  install_requires=['jupyter-server-proxy','pyyaml'],
)

# requires: https://github.com/gitpod-io/openvscode-server
#    https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-${RELEASE_TAG}/openvscode-server-${RELEASE_TAG}-linux-${arch}.tar.gz
# server.sh in PATH