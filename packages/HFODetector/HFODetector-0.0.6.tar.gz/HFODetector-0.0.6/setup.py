import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HFODetector",
    version="0.0.6",
    author="Taylor Chung",
    author_email="taylorchung@ucla.edu",
    description="Package for detecing HFOs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={ },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'mne',
        'numpy',
        'scipy',
        'matplotlib',
        'pandas'
    ],
    include_package_data=True,
    python_requires=">=3.6",
)