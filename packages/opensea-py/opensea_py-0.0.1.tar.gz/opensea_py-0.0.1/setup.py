import setuptools

# python setup.py sdist bdist_wheel
# twine upload dist/* && rm -rf build dist *.egg-info

setuptools.setup(
    name="opensea_py",
    version="0.0.1",
    author="RA",
    author_email="numpde@null.net",
    keywords="python sdk opensea nft",
    description="Python SDK for OpenSea.",
    long_description="Python SDK for OpenSea. [Info](https://github.com/numpde/opensea_py).",
    long_description_content_type="text/markdown",
    url="https://github.com/numpde/opensea_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[],

    # Required for includes in MANIFEST.in
    #include_package_data=True,

    test_suite="nose.collector",
    tests_require=["nose"],
)
