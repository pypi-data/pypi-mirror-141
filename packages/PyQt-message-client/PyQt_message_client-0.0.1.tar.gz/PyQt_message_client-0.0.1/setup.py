from setuptools import setup, find_packages

setup(name="PyQt_message_client",
      version="0.0.1",
      description="Message_Client",
      author="Pavel Nedoshivin",
      author_email="pnedoshivin@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
