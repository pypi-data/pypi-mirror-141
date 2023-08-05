from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements.txt') as f:
#     required = f.read().splitlines()


setup(
        name="xcash",
        version="0.0.3",
        packages=find_packages(),
        description="XCASH ecosystem wrapper",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/X-CASH-official/XCASH-Ecosystem-api-wrapper",
        author="AnimusXCASH",
        author_email="lovro@gmail.com",
        license="MIT",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
        ],
        install_requires=[
            "requests"
        ],
        )
