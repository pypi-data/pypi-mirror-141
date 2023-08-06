import os

from setuptools import setup

version = os.getenv("GITHUB_REF", "refs/tags/v0.0.0").split("/")[-1]
print(f"Building version: {version}")

setup(
    name="PiKVM utils",
    version=version,
    description="Quick and easy PiKVM setup script",
    author="Mads Ynddal",
    author_email="mads@ynddal.dk",
    url="https://github.com/Baekalfen/pikvm-utils",
    py_modules=["pikvm_utils"],
    entry_points={
        "console_scripts": ["pikvm_utils=pikvm_utils:main", ],
    },
    install_requires=[
        "paramiko",
        "requests",
    ],
)
