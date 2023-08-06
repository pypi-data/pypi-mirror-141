from setuptools import setup, find_packages


setup(name="my_first_training_messenger_server",
      version="0.1",
      description="Messenger Server",
      author="Zakharov Vladimir",
      author_email="vovazakharov2@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'])
