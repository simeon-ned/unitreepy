import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyunitree", 
    version="0.0.1",
    author="Simeon Nedelchev",
    author_email="s.nede@gmail.com",
    description="A package provide parsers and handlers of Unitree robots",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 
    ],
    packages=setuptools.find_packages(),
    # install_requires = ['']
    python_requires=">=3.6",
)
