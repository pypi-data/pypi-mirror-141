# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

project_url = "https://gitlab.com/cbjh/memgen/py-memgen"

with open("README.md", "r", encoding="utf-8") as fp:
    readme_content = fp.read()
    fixed_links = re.sub(r"!\[([^\]]*)\]\(([^)]*)\)", r"![\1]({}/-/raw/master/\2)".format(project_url), readme_content)

setup(
    name="memgen",
    scripts=['src/memgen/bin/memgen'],
    author="Maciej Wójcik",
    author_email="w8jcik@gmail.com",
    description="Calls MemGen service located at http://memgen.uni-saarlad.de/api",
    long_description=fixed_links,
    long_description_content_type="text/markdown",
    url=project_url,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[],
)
