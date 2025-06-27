#!/usr/bin/env python
import sys
from setuptools import setup, find_packages

sys.path.insert(0, "src")
from version import VERSION

setup(
    name="videocompressor",
    version=VERSION,
    description="Compress videos to any file size using a clean PyQt6 GUI.",
    author="4ndr0666",
    author_email="none@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.6.1",
        "requests>=2.31.0",
        "notifypy>=1.0.4",
        "psutil>=5.9.8",
    ],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: Qt",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "videocompressor=main:main",
        ],
    },
    python_requires=">=3.11",
    zip_safe=False,
)
