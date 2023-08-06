import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loguwant",
    version="0.0.2",
    author="Yash Goyal",
    author_email="yashgoyalcs@gmail.com",
    description="It is a Python package that enables you to log only what you want",
    long_description="""It's a Python package that enables you to log only what you want. It creates logger, using which
    you can see the logs of the modules written by you separately.
    
    For this we have to defined log level of root logger and log Level of the modules you write and whose logs you want 
    to print as environment variables ROOT_LOG_LEVEL and CURRENT_LOG_LEVEL respectively. 
    
    We can also switch this functionality by using LOG_DEPTH environment variable.""",
    long_description_content_type="text/markdown",
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
