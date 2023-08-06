from setuptools import setup
from pynotio.version import version

with open('README.md', 'r') as fh:
    long_description = fh.read()

requirements = ['requests<=2.27.1']


setup(name='pynotio',
      version=version,
      description='Python wrapper around official Notion API for easy life',
      long_description=long_description,
      packages=['pynotio'],
      author='Ruslan Abkadirov',
      author_email='rusabk@yandex.ru',
      url='https://github.com/Ruslanabk/PyNotio',
      zip_safe=False,
      install_requires=requirements,
      classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
      ],
      python_requires='>=3.6'
)