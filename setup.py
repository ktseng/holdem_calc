import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='holdem_calc',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/RoelandMatthijssens/holdem_calc',
    license='MIT',
    author='Enermis',
    author_email='roeland.matthijssens@gmail.com',
    description='''Holdem Calculator library''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)
