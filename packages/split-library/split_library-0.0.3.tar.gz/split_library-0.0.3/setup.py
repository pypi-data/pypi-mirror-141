from setuptools import setup

setup(
    name='split_library',
    version='0.0.3',
    description='Split library for VRP developed by Jamie',
    py_modules=['split_library', 'guide'],
    install_requires=[
        "numba ~= 0.55.1",
    ],
    package_dir={'': 'src'},
    url="",
    author="Jamie Nguyen",
    author_email="thangnmtfac@gmail.com"
)
