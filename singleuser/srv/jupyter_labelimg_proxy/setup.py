from setuptools import setup, find_packages

setup(
    name="jupyter-labelimg-proxy",
    packages=find_packages(),
    version='0.1.0',
    description="Jupyter extension to run lableImg using VNC",
    keywords=["Jupyter"],
    entry_points={
        'jupyter_serverproxy_servers': [
            'labelimg = jupyter_labelimg_proxy:setup_labelimg',
        ]
    },
    install_requires=['jupyter-server-proxy>=1.4.0'],
    package_data={'jupyter_labelimg_proxy': ['resources/*']},
    include_package_data=True,
    zip_safe=False
)
