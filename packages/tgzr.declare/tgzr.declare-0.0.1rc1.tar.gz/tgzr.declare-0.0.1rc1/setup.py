import os
import sys

# NB: tgzr is using native namespace pacakges !
# see: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#creating-a-namespace-package
from setuptools import setup, find_namespace_packages

README = os.path.join(__file__, "..", "README.md")

with open(README, "r") as fp:
    long_description = fp.read()
setup(
    name="tgzr.declare",
    description="Component UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TGZR/tgzr.declare",
    author='Damien "dee" Coureau',
    author_email="dee909@gmail.com",
    license="LGPLv3+",
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        # "Topic :: System :: Shells",
        # "Intended Audience :: Developers",
        # 'Intended Audience :: End Users/Desktop',
        # "Operating System :: Microsoft :: Windows :: Windows 10",
        # 'Programming Language :: Python :: 2.7',
        # "Programming Language :: Python :: 3.7",
        # "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    # keywords="",
    install_requires=[
        "six",
        "pydantic",
    ],
    extras_require={
        "qtpy": [
            "qtpy",
            "qtawesome",
            "qt-material",
            "markdown",
            "pygments",
        ],
        "PySide2": [
            "PySide2",
        ],
        "dev": [
            "tox",
            "pytest",
            "pytest-cov",
            "flake8",
            "black",
            "twine",
        ],
    },
    python_requires=">=3.7",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    package_data={
        "": ["*.css", "*.png", "*.svg", "*.gif", "*.mp3"],
    },
)
