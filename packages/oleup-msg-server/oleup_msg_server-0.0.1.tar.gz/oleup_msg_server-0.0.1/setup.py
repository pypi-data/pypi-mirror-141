from setuptools import setup, find_packages

setup(name="oleup_msg_server",
      version="0.0.1",
      description="message_server",
      author="Ole_Up",
      author_email="oleup@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
