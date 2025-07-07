from setuptools import setup, find_packages

setup(
    name="videocompressor",
    version="1.0.1",  # ← bumped
    description="Compress videos to any file size using a PyQt6 GUI.",
    author="4ndr0666",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.6.1",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "videocompressor=main:main"
        ]
    },
)
