import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="easyTX",
    version="2.0",
    description="Module to exchange data in any form (video or string) from one PC to another over the same network.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/VDHARV/easyTX-2.0",
    author="VDHARV",
    author_email="vdharv4bharat@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["easyTX"],
    include_package_data=True,
    install_requires=["opencv-python", "numpy"],
)