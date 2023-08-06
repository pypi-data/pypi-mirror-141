from setuptools import setup, find_packages

setup(name="PyQt_server_client",
      version="0.0.1",
      description="Server_Client",
      author="Pavel Nedoshivin",
      author_email="pnedoshivin@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
