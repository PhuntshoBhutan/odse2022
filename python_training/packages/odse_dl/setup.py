import setuptools
from pathlib import Path
from odse_dl import __version__

root_dir = Path(__file__).parent

with open(root_dir.joinpath('README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='odse_dl',
    version=__version__,
    description='OpenDataScience Europe Deep Learning Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/olegsson/odse2022_dl-training',
    packages=setuptools.find_packages(),
    package_data={},
    scripts=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
