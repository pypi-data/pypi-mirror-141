from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='drtest',
    version='0.0.1',
    description='This is a test module that currently performs data reduction on arrays by different methods.',
    py_modules=['drtest'],
    package={'': 'src'},
    license_files = ('LICENSE',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy ~= 1.19.5",
        "matplotlib ~= 3.3.3",
        "pyabf ~= 2.3.5",
        "check-manifest ~= 0.47"
    ],   
    url="https://github.com/MS44neuro/drtest",
    author="MSneuro",
)