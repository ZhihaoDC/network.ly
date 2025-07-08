from setuptools import setup, find_packages

setup(name="src", 
    packages=['src'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],)