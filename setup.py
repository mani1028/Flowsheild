"""
Setup configuration for FlowShield package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flowshield",
    version="1.0.0",
    author="FlowShield",
    description="Ultra-lightweight, high-performance traffic control middleware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flowshield",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Flask>=1.1.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.10"],
    },
)
