from setuptools import setup, find_packages
# cd d:\projects\nbp-rates-creator
# pip install -e .


setup(
    name="nbp_rates",
    version="0.1.4",
    # find_packages() automatically finds 'nbp_rates' and 'nbp_rates.currencies'
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Since you used only standard libraries (urllib, json, datetime), 
        # no external dependencies are strictly required here.
    ],
    author="Next Level Sense",
    description="A modular library for NBP exchange rates with offline and online support.",
    python_requires=">=3.6",
)
