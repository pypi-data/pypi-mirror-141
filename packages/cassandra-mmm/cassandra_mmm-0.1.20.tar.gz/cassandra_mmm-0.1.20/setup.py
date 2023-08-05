"""The setup script."""
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = "0.1.20"
PACKAGE_NAME = "cassandra_mmm"
AUTHOR = "Cassandra"
URL = "https://github.com/Tsurty/cassandra"
LICENSE = "MIT"
DESCRIPTION = "Cassandra library"
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf8')
LONG_DESC_TYPE = "text/markdown"
#INSTALL_REQUIRES = [
    #"numpy",
    #"pandas",
    #"matplotlib",
    #"statsmodels",
    #"typing",
    #"sklearn",
    #"seaborn",
    # "prophet"
#]
setup(name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    #author_email=AUTHOR_EMAIL,
    url=URL,
    #install_requires=INSTALL_REQUIRES,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data = {
    '': ['*.txt', '*.csv'],
    },
    include_package_data=True
)