import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="MR_Package",
    version="0.0.1",
    author="Manuel Alexander Christoph Raffl",
    author_email="manuraffl003@gmail.com",
    description="A small package for easy file IO and maths",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuraffl30/RA_Rechner",
    project_urls={
        "Bug Tracker": "https://github.com/manuraffl30/RA_Rechner/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires="==3.8",
    install_reqires=[
        "kivy[full] = 2.0.0"
    ])