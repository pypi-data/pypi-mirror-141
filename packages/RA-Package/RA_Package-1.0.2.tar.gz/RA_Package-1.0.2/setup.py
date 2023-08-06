import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="RA_Package",
    version="1.0.2",
    author="Manuel Alexander Christoph Raffl",
    author_email="manuraffl003@gmail.com",
    description="Backend Library for RA-Rechner",
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
    packages=setuptools.find_packages(where="src"),)