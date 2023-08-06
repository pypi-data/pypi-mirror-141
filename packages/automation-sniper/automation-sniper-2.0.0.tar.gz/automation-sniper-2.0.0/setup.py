import os
import pathlib
from setuptools import setup, find_packages
from service.__version__ import __version__
from version_bump import VersionBump

# The directory containing this file
HERE = pathlib.Path(__file__).parent

pkg_vars = {}

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="automation-sniper",
    version=__version__,
    python_requires=">=3.7",
    description="Tool to convert Open API / Swagger specifications to automation framework",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pankajnayak1994/automation-sniper",
    author="Pankaj Kumar Nayak",
    author_email="nayakpankaj2015@gmail.com",
    license="Apache-2.0 License",
    keywords="",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Jinja2==3.0.3",
        "PyYAML==6.0",
        "coloredlogs==14.0",
        "flake8==3.8.3",
        "flask==1.1.2",
        "flask-restful==0.3.9",
        "pytest==5.4.3",
        "requests==2.27.1",
        "pytest==5.4.3",
        "validators==0.18.2",
        "gitchangelog==3.0.4"
    ],
    entry_points={
        "console_scripts": [
            "automation-sniper=service.__main__:main",
        ]
    },
)
