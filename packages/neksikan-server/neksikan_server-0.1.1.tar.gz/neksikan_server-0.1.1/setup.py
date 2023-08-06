from setuptools import setup, find_packages

setup(name="neksikan_server",
      version="0.1.1",
      description="neksikan_server",
      author="Gordon Freeman",
      author_email="halflife_3@valve.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
