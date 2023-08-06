import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loguwant",
    version="0.0.3",
    author="Yash Goyal",
    author_email="yashgoyalcs@gmail.com",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/yashgoyal07/loguwant",
    project_urls={
        "Bug Tracker": "https://github.com/yashgoyal07/loguwant/issues",
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
