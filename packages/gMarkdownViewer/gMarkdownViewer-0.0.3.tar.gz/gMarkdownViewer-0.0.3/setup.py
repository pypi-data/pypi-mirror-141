#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 22 February, 2022
"""
from setuptools import setup

setup(
    name = "gMarkdownViewer",
    version = "0.0.3",
    author = "Ben Knisley",
    author_email = "benknisley@gmail.com",
    description = "A simple GUI application for viewing Markdown files.",
    url = "https://git.benknisley.com/benknisley/MarkdownViewer",
    license = "MIT",
    keywords = "markdown",
    install_requires=[
        'Markdown==3.3.4', 
        'PyGObject==3.40.1'
    ],
    packages=["MarkdownViewer",],
    long_description="A simple Markdown viewer, made with Python, GTK, and Webkit.",
    
    ## Set up console scripts files
    entry_points = {
        'console_scripts': [
            'markdownviewer = MarkdownViewer:main',
        ],              
    },

    ## Include aux package files (in MarkdownViewer folder)
    include_package_data=True,
    package_data={'MarkdownViewer': ['highlight_js.html', 'place_holder.md']},

    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)
