
import setuptools


setuptools.setup(
    name="SHU_pipytest",
    version="0.0.6",
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
    package_dir={"": "SHU_pipytest"},
    packages=setuptools.find_packages(where='SHU-cxpipytest'),
    python_requires=">=3.6",
)