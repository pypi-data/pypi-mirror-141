from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='OWN_THE_PLANET_BOARD_GAME_EDITION',
    version='1',
    packages=['OWN_THE_PLANET_BOARD_GAME_EDITION'],
    url='https://github.com/DigitalCreativeApkDev/OWN_THE_PLANET_BOARD_GAME_EDITION',
    license='MIT',
    author='DigitalCreativeApkDev',
    author_email='digitalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of the game "Own The Planet - Board Game Edition". The game '
                'involves the player and CPU competing to be the richest in the planet.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "OWN_THE_PLANET_BOARD_GAME_EDITION=OWN_THE_PLANET_BOARD_GAME_EDITION.OwnThePlanetBoardGameEdition:main",
        ]
    }
)