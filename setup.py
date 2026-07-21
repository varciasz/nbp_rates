from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="nbp_rates",
    version="1.4.20260721",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    author="Sebastian Kowalik",
    description="A modular library for NBP exchange rates with offline and online support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/varciasz/nbp_rates",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Polish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="nbp exchange rates currency forex polska pln",
    project_urls={
        "Bug Tracker": "https://github.com/varciasz/nbp_rates/issues",
        "Source Code": "https://github.com/varciasz/nbp_rates",
    },
)
