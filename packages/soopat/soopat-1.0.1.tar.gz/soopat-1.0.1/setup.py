import os
import json
import codecs
from pathlib import Path
from setuptools import setup, find_packages


BASE_DIR = Path(__file__).resolve().parent
version_info = json.loads(BASE_DIR.joinpath('soopat', 'version', 'version.json').read_text())


setup(
    name=version_info['prog'],
    version=version_info['version'],
    author=version_info['author'],
    author_email=version_info['author_email'],
    description=version_info['desc'],
    long_description=codecs.open(os.path.join(BASE_DIR, 'README.md'), encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/soopat',
    project_urls={
        'Documentation': 'https://soopat.readthedocs.io',
        'Tracker': 'https://github.com/suqingdong/soopat/issues',
    },
    license='BSD License',
    install_requires=codecs.open(os.path.join(BASE_DIR, 'requirements.txt'), encoding='utf-8').read().split('\n'),
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'soopat = soopat.bin.main:main',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ]
)
