from distutils.core import setup
setup(name='pyLucidIo',
      version='2.1.1',
      description='LucidControl USB IO Module Package',
      author='Klaus Ummenhofer',
      url='http://www.lucid-control.com',
      #py_modules=['lucidIo'],
      install_requires=["pyserial"],
      packages=['lucidIo'],
      )
