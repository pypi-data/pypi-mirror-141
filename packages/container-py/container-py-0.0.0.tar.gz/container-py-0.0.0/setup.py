from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    name='container-py',  # Required
    version='0.0.0',  # Required
    description="the missing container python sdk",  # Optional
    url='https://github.com/danielbraun-org/container',  # Optional
    author='Daniel Braun',  # Optional

    author_email='braundaniel@live.com',  # Optional

    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required
)
