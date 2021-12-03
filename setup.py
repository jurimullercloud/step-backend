import setuptools
import os


with open("./requirements.txt", "r") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="step-backend",
    description="Backend api for step project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=required
)