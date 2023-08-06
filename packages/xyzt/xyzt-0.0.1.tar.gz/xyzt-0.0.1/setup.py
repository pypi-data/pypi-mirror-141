from setuptools import setup

long_description = None
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="xyzt",
    packages=["xyzt"],
    version="0.0.1",
    license="MIT",
    description="Compute and plot timing scalings for functions with numpy array inputs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nosarthur/xyzt",
    platforms=["linux", "osx", "win32"],
    keywords=["bash"],
    author="Dong Zhou",
    author_email="zhou.dong@gmail.com",
    python_requires="~=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
