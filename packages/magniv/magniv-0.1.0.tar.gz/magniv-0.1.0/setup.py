from setuptools import setup, find_packages

setup(
    name="magniv",
    version="0.1.0",
    py_modules=["magniv"],
    packages=find_packages(include=['magniv']),
    install_requires=[
        "Click",        
    ],
    entry_points={
        "console_scripts": [
            "magniv-cli = magniv.scripts.magniv:cli",
        ],
    },
)
