from setuptools import setup, find_packages


# Get the version number from the version.py file
with open("gershgorin/version.py") as f:
    __version__ = f.read().split()[-1].strip("'")

setup(
    name="gershgorin",
    version=__version__,
    description="Visualize the Gershgorin discs that bound the spectrum of a square matrix.",
    url="https://github.com/v715/gershgorin",
    author="Vivek Gopalakrishnan",
    author_email="vivekg@mit.edu",
    license="MIT",
    packages=find_packages(),
    install_requires=["matplotlib", "numpy", "adjustText"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
