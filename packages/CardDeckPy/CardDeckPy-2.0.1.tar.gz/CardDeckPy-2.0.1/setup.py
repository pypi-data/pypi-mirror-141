import setuptools
from PyCardDeck import __version__

with open("README.md", "r") as fhandle:
    long_description = fhandle.read()

setuptools.setup(
    name="CardDeckPy",
    version=__version__,
    author="Israel Waldner",
    author_email="imky171@gmail.com",
    description="A library for working with cards, decks, and hands in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://replit.com/@IsraelW/Card-Deck-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
)
