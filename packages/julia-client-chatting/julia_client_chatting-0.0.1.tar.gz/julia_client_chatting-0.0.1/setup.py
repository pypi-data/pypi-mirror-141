from setuptools import setup, find_packages

setup(name="julia_client_chatting",
      version="0.0.1",
      description="Mess Client",
      author="Zakharova Julia",
      author_email="sorulai@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )