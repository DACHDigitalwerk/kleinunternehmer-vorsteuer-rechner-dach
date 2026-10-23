# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="kleinunternehmer-dach",
    version="1.0.0",
    description="DACH Kleinunternehmer- & USt-Vorsteuer-Rechner 2026 (EU-Richtlinie DE, AT, CH)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="DACH Digitalwerk",
    author_email="dach.digitalwerk@gmail.com",
    url="https://dach-digitalwerk.netlify.app/kleinunternehmer-vorsteuer-rechner/",
    packages=find_packages(exclude=["tests*", "examples*"]),
    entry_points={
        "console_scripts": [
            "dach-kleinunternehmer=kleinunternehmer_dach.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
