import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.3'
PACKAGE_NAME = 'pygame_easy_btn'
AUTHOR = 'Amin shahrabi'
AUTHOR_EMAIL = 'shahrabiamin70@gmail.com'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'python package for pygame to make buttons'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    "pygame"
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )