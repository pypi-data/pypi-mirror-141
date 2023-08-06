from setuptools import setup, find_packages

setup(name="vl_message_server",
      version="0.0.1",
      description="Message Server",
      author="Vitalii Loboda",
      author_email="vl@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      #scripts=['server/server_run']
      )
