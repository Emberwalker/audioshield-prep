import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audioshield-prep",
    version="0.0.1",
    author="Robert T",
    author_email="arkan@drakon.io",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emberwalker/audioshield-prep",
    packages=setuptools.find_packages(),
    install_requires=["pydub >= 0.23, < 0.24"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
