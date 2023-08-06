from setuptools import setup
from pathlib import Path

directory = Path(__file__).parent

setup(
    name='sformat',
    version='0.1.0',
    packages=['sformat'],
    entry_points={
        "console_scripts": ["sformat=sformat.main:main"],
    },
    author='Pursuit',
    author_email='fr.pursuit@gmail.com',
    description='Format an input stream using the section character',
    long_description=(directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://github.com/',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
