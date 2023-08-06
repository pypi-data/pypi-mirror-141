from setuptools import setup, find_packages

setup(name="ng_client",
      version="1.0.0",
      description="ng_client",
      author="Oz Oz",
      author_email="oz.oz@oz.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
