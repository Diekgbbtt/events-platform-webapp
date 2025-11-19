from setuptools import setup, find_packages

setup(
    name="ocl-py",
    version="0.5.0",
    description="Object Constraint Language implementation for Python",
    packages=find_packages(),
    install_requires=[
        "antlr4-python3-runtime==4.13.0",
        "forbiddenfruit==0.1.4",
        "pytest==7.2.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)