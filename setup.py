"""
Setup configuration for FlowShield package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flowsh",
    version="1.0.0",
    author="FlowShield Contributors",
    author_email="opensource@flowshield.dev",
    description="The fastest and simplest way to protect your Python app from traffic spikes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pravalika/flowshield",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=1.1.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.10"],
    },
)
