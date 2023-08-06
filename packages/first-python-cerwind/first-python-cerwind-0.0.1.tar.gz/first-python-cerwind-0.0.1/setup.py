from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "My first Python package"
LONG_DESCRIPTION = "My first Python package with a slightly longer description"

setup(
    name="first-python-cerwind",
    version=VERSION,
    author="Charlie Day",
    author_email="<charliemday31@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package
    keywords=["python", "first package"],
    classifiers=[],
)
