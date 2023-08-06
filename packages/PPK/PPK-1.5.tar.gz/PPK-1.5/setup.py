from setuptools import setup

setup(name='PPK',
      version="1.5",
      packages=['PPK', 'PPK.Tools', 'PPK.Exceptions'],
      url='https://github.com/MHProDev/PyRoxy',
      license='MIT',
      author="FFPS",
      install_requires=[
          "maxminddb>=2.2.0", "requests>=2.27.1", "yarl>=1.7.2",
          "pysocks>=1.7.1"
      ],
      include_package_data=True,)
