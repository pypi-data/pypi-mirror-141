from setuptools import setup

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="erengazimutlu-cs453-HW1",
    author="Erengazi Mutlu",  # TODO: Write your name
    version="2.3.4",
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
