from setuptools import setup

setup(
    name="ekg-cs458-dict",
    author="Ege Kaan Gürkan",
    version="0.0.3",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",
    description="A package for my CS453 Homework 1."
)
