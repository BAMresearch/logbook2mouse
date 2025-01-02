from setuptools import setup, find_packages

setup(
    name='logbook2mouse',  # Updated project name
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'attrs',
        'openpyxl'
    ],
)