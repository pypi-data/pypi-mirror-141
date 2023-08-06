from setuptools import setup, find_packages


setup(
    name='example_publish_pypi_first_time',
    version='1.0.0',
    license='MIT',
    author="Nihal Todankar",
    author_email='todankarnihal18@gmail.com',
    packages=find_packages('src/example_package'),
    package_dir={'': 'src'},
    url='https://github.com/Nihal-Git/example-package',
    keywords='example project'
)