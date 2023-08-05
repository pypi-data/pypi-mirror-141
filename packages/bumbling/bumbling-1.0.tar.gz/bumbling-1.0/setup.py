#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2022-03-03

from setuptools import setup, find_packages

setup(
    name="bumbling",
    version="1.0",
    license="MIT",
    author="Jonathan Roth",
    author_email="JonathanRoth@protonmail.com",
    py_modules=["src.bumbling"],
    url="https://github.com/JonathanRoth13/bumbling",
    install_requires=["PyExifTool"],
    entry_points={"console_scripts": ["bumbling=src.bumbling:main"]},
)
