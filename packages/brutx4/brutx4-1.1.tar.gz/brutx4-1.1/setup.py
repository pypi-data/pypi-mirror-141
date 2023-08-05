import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brutx4",
    version="1.1",
    author="Rakib Hossain",
    author_email="rakib4ggp@gmail.com",
    description="A Bruteforce Package by Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['brutx4'],
)
