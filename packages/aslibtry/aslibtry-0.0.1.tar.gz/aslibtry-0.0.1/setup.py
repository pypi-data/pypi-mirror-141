from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='aslibtry',
  version='0.0.1',
  description='A very basic calculator',
  long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
  url='',  
  author=' Aslı Nur ',
  author_email='aslinurt85@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)