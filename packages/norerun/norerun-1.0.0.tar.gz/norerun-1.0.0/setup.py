import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="norerun",
    version="1.0.0",
    author="Albert",
    metadata_version="1.0",
    author_email="lahat.albert@gmail.com",
    description="Backup to store results of functions, so they do not need to be rerun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aLahat/remember/issues",
    project_urls={
        "Bug Tracker": "https://github.com/aLahat/remember/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)