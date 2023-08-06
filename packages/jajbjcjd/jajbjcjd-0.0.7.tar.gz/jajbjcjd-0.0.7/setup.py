
import setuptools


setuptools.setup(
    name="jajbjcjd",
    version="0.0.7",
    author="XHLin",
    author_email="xhaughearl@gmail.com",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    install_requires = [

        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "jajbjcjd"},
    packages=setuptools.find_packages(where='jajbjcjd'),
    python_requires=">=3.6",
)