import setuptools

DESCRIPTION = 'Creates a static .html file with charts using Google Charts API'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plot2html",
    version="0.0.8",
    author="Rafael Rodrigues Troiani",
    author_email="rafael.r.troiani@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    url='https://github.com/rafatro/plot2html',
    install_requires=['pandas','datetime'],
    keywords=['python', 'Google Charts', 'html'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ]
)