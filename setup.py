from setuptools import setup

long_description = """nlab utils
"""

setup(
    name='nlabutils',
    version='0.1',
    url='https://github.com/gavin-s-smith/nlabutils',
    license='MIT',
    py_modules=['nlabutils'],
    author='Gavin Smith',
    author_email='gavin.smith@nottingham.ac.uk',
    install_requires=['numpy','pandas','sklearn','rpy2','statsmodels'],
    description='Time series decomposition utilities, including an R wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='R, time series decomposition',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Intended Audience :: Developers']
)
