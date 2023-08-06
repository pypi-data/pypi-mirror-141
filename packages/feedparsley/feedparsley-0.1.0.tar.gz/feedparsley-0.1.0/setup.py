import re, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("./feedparsley/__init__.py", "r") as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2)

# package:
# python3 setup.py sdist bdist_wheel
# upload:
# twine upload --repository dist/*

setuptools.setup(
    name="feedparsley",
    version=VERSION,
    author="ibz",
    author_email="feedparsley@ibz.me",
    description="Parse feeds using feedparser or xml.etree.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibz/feedparsley",
    packages=setuptools.find_packages(),
    python_requires='>3.7.0',
    install_requires=[
        "bs4",
        "feedparser",
        "python-dateutil",
        "requests",
    ],
    extras_require={
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "feedparsley = feedparsley.feedparsley:main",
        ]
    },
)