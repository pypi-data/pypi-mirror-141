import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().strip().split('\n')

setuptools.setup(
    name="rslurm",
    version="0.0.1",
    author="Yasas Senarath",
    description="Helps to run remote jobs easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ysenarath/rslurm",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
