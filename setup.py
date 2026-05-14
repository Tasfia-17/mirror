from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("VERSION", "r") as f:
    version = f.read().strip()

setup(
    name="mirror-ai",
    version=version,
    description="60 seconds of voice into 50 pieces of content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tasfia-17",
    author_email="rifatasfiachowdhury@gmail.com",
    url="https://github.com/Tasfia-17/mirror",
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt")],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "mirror=mirror:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
