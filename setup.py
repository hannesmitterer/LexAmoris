from setuptools import setup, find_packages

setup(
    name="lexamoris-internodal",
    version="0.1.0",
    description="Internodal connection streams for LexAmoris bio-synthetic operating system",
    author="Hannes Mitterer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio>=1.60.0",
        "grpcio-tools>=1.60.0",
        "protobuf>=4.25.8",
        "websockets>=12.0",
    ],
    python_requires=">=3.8",
)
