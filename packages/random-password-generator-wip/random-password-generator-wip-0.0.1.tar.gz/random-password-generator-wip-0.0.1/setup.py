  
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='random-password-generator-wip',
  version='0.0.1',
  description='A very basic password generator app',
  long_description=open('README.txt').read() + '\n\n' + open('Changelog.md').read(),
  url='',
  author='Shivam Khandelwal',
  author_email='shivamkhandelwal555@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='passowrd, password-generator',
  packages=find_packages(),
  install_requires=['']
)