# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='order2',
    version='0.4.0',
    py_modules=['order2'],
    install_requires=['matplotlib', 'ac-electricity'],
    description='An educational module about second-order systems',
    author='Fabrice Sincère',
    author_email='fabrice.sincere@ac-grenoble.fr',
    maintainer='Fabrice Sincère',
    maintainer_email='fabrice.sincere@ac-grenoble.fr',
    url='https://framagit.org/fsincere/order2',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: French",
    ],
    python_requires='>=3',)
