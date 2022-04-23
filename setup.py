import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="christinaa-the-pink-coder",
    version="0.0.1",
    author="Christina Liu",
    author_email="christinaa.danks@me.com",
    description="A fun platform game built with pyGame",
    long_description='Please read the README file for more information',
    long_description_content_type="text/markdown",
    url="https://github.com/christinaadanks/christinaa_the_coder_game",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "game_code"},
    packages=setuptools.find_packages(where="game_code"),
    python_requires=">=3.6",
)