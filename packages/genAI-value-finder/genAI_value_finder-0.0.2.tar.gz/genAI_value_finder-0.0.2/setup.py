from setuptools import setup
from setuptools import find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='genAI_value_finder',
  version='0.0.2',
  description='find the values of variables in given equation',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Dhruv A. Gandhi',
  author_email='dhruvalkeshkumargandhi2000@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='values', 
  
  packages=find_packages(),
  install_requires=[''] 
)