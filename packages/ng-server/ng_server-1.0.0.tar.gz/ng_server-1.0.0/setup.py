from setuptools import setup, find_packages

setup(name="ng_server",
      version="1.0.0",
      description="ng_server",
      author="Oz Oz",
      author_email="oz.oz@oz.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']      
      )
