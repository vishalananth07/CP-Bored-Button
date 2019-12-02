import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cpboredbutton",
    version="1.0",
    scripts=['scripts/cpboredbutton'],
    author="vishalananth, anishbadri",
    author_email="vishalananth98@gmail.com, anishbadhri@gmail.com",
    description="Competitive programming problem recommendation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishalananth07/CP-Bored-Button",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
)
