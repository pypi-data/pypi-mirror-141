import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Read_File_Devika_P",
    version="0.2",
    author="Devika Paranjpe",
    author_email="",
     description='A Python package to read data from .yaml and .cfg or config files. It creates .json and .env file'
                'to the input file and writes data. Also loads environment variables as per configuration file. ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zekardo/MyProjects.git",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
 
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)