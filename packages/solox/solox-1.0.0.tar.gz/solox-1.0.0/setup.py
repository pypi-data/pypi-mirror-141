import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solox",
    version="1.0.0",
    author="Chen Hongqing",
    author_email="",
    description="Simple Test In SoloX !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rafa0128/SoloX",
    packages=setuptools.find_packages(),
    install_requires=['flask>=2.0.1'],
    entry_points={
        'console_scripts': [
            'solox=solox:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)