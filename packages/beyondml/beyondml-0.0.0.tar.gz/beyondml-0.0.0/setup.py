from setuptools import setup
from beyondml import __version__

setup(
    name = 'beyondml',
    version = __version__,
    url = 'https://github.com/Beyond-ML-Labs/beyondml',
    packages = [
        'beyondml'
    ],
    author = 'Beyond ML Labs',
    author_email = 'staff@squared.ai',
    description = 'Beyond ML Packaged Technology',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    license = 'GPL v3.0',
    license_files = 'LICENSE'
)
