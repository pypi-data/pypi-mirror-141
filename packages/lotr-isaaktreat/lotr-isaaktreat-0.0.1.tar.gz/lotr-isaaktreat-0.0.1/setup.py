from importlib.metadata import entry_points
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lotr-isaaktreat",
    version="0.0.1",
    author="Isaak Treat",
    author_email="isaaktreaty@gmail.com",
    description="SDK for Lord of the Rings API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isaak-treat/LotRIsaakSDK",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'lotr=client.client:__main__'
        ]
    }

)