from setuptools import setup

 setup(
   name='simplefetch',
   version='0.1.0',
   author='Ercin TORUN',
   author_email='ercintorun@gmail.com',
   packages=['simplefetch'],
   scripts=['bin/script1','bin/script2'],
   url='http://pypi.python.org/pypi/simplefetch/',
   license='LICENSE.md',
   description='Simplified Paramiko Library to Fetch Data From MultiVendor Network Devices',
   long_description=open('README.md').read(),
   install_requires=[
       "paramiko",
   ],
)
