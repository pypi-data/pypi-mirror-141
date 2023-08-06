"""Setup script for aws-nsm-interface."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-nsm-interface-verifiably",
    version="1.0.0",
    author="Verifiably",
    author_email="atul@verifiably.com",
    description="Native Python interface for the AWS Nitro Secure Module (NSM)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/verifiably/aws-nsm-interface-verifiably",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'cbor2>=5.2.0',
        'ioctl-opt>=1.2.2'
    ],
)
