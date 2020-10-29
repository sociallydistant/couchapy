import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="couchapy",
    version="0.0.1-alpha.2",
    author="Lee Lunn",
    author_email="lee.lunn@gmail.com",
    description="Library for interacting with CouchDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sociallydistant/couchapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",

        "License :: OSI Approved :: Apache Software License",

        "Topic :: Database",
        "Topic :: Software Development :: Libraries",

        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",

        "Operating System :: OS Independent",

        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        "Natural Language :: English",
    ],
    python_requires='>=3.6',
)
