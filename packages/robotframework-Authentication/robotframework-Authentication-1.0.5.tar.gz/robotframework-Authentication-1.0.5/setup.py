import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="robotframework-Authentication",
    version="1.0.5",
    description="Permet de se connecter à un portail.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="ADSN GROUP",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Authentication"],
    include_package_data=True,
)
