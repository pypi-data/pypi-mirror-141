import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phaseportrait",
    version="1.0.4",
    author="Víctor Loras & Unai Lería",
    author_email="vhloras@gmail.com, unaileria@gmail.com",
    description="A python package for visualizing non-linear dynamics and chaos. (2D phase portraits, 3D chaotic trajectories, Maps, Cobweb plots...)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phaseportrait/phaseportrait",
    project_urls={
        "Documentation": "https://phaseportrait.github.io/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
