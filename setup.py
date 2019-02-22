from setuptools import setup, find_packages

setup(
    name='sarnieploy',
    version='0.0.1',
    description='Deploy a Wargery generated war artifact to a Jetty server',
    author='Nicolo Maioli',
    author_email='nicolomaioli@gmail.com',
    install_requires=[
        'wargery==1.0.0'
    ],
    dependency_links=[
        'https://github.com/nicolomaioli/wargery/tarball/master#egg=wargery-1.0.0'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['sarnieploy=sarnieploy.sarnieploy:deploy_to_server']
    }
)
