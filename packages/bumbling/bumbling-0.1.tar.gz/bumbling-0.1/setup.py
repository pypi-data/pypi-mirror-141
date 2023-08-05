from setuptools import setup, find_packages

setup(
name="bumbling",
version="0.1",
author="Jonathan Roth",
author_email="JonathanRoth@protonmail.com",
url="https://github.com/JonathanRoth13/bumbling",
packages=find_packages(),
install_requires=["PyExifTool"],
entry_points={
        'console_scripts': ['bumbling=bumbling:main']
    }
)
