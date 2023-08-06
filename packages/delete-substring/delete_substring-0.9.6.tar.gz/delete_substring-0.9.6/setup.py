import setuptools


setuptools.setup(
    name="delete_substring",
    version="0.9.6",
    author="",
    author_email="",
    description="Simple library for delete substring",
    long_description="Simple library for delete substring",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
