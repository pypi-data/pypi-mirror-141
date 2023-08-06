from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="bulut-cicd-test",
    author="Bulut Gözübüyük",  # TODO: Write your name
    version="2.0.3",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
