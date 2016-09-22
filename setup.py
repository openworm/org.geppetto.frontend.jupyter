import setuptools

setuptools.setup(
    name="geppetto_connector",
    version='0.1.0',
    url="http://example.org",
    author="John Doe",
    description="Amazing nbextension",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
)