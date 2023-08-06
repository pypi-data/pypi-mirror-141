from setuptools import setup, find_packages
from podpointclient.version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="podpointclient",
    version=VERSION,
    author="Matthew Rayner",
    author_email="hello@rayner.io",
    description="A simple API client for Pod Point (https://pod-point.com) aimed at home users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattrayner/podpointclient",
    project_urls={
        "Bug Tracker": "https://github.com/mattrayner/podpointclient/issues",
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=(
        find_packages(exclude=['tests']) +
        find_packages(where="./podpointclient") +
        find_packages(where="./podpointclient/helpers")
    ),
    python_requires=">=3.7",
    keywords='Pod Point PodPoint',
    include_package_data=True,
)