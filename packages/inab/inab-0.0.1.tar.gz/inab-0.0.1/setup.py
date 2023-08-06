import setuptools

with open("/content/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inab", # Replace with your own username
    version="0.0.1",
    author="Rami Mahmmoud",
    author_email="rizr93172@gmail.com",
    description="A library for decoding a byte marked as a string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inab/i nab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)