import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="fileStorage3",
    version="0.0.3",
    author="edcilo",
    description="storage handler for multiple services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    exclude=["test"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    packages=["fileStorage3"],
    package_dir={"":"src"},
    install_requires=[
        "boto3>=1.6.0",
    ],
)
