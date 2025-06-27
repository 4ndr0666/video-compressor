from setuptools import setup, find_packages

setup(
    name="videocompressor",
    version="1.0.0",
    description="Compress videos to a target size using FFmpeg",
    author="4ndr0666",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.6.1",
        "requests>=2.31.0",
        "psutil>=5.9.8",
    ],
    entry_points={"gui_scripts": ["videocompressor=main:main"]},
)
