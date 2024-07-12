from setuptools import setup

setup(
    name="smart-buildings-rating-calculator",
    author="Centre for Net Zero",
    author_email="data@centrefornetzero.org",
    description="The calculation to generate a smart building rating",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/centrefornetzero/smart-building-rating-calculator",
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.11",
)
