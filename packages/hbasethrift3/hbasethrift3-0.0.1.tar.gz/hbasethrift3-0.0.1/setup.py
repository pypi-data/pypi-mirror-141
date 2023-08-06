import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


VERSION = '0.0.1'


setuptools.setup(
    name="hbasethrift3",
    version=VERSION,
    author="dfore",
    author_email="darrenfore@gmail.com",
    description="hbasethrift3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shawjan/hbasethrift3",
    project_urls={
        "Bug Tracker": "https://github.com/shawjan/hbasethrift3/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
)