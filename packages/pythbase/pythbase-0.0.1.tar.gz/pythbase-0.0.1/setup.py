import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


VERSION = '0.0.1'


setuptools.setup(
    name="pythbase",
    version=VERSION,
    author="darrenfore",
    author_email="darrenfore@gmail.com",
    description="Python connection pool for hbase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shawjan/pythbase",
    project_urls={
        "Bug Tracker": "https://github.com/shawjan/pythbase/issues",
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