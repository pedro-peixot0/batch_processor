from setuptools import setup, find_packages

setup(
    name='batch_processor',
    version='0.1',
    packages=find_packages(),
    author='Pedro Peixoto',
    author_email='pedroamadopeixoto@gmail.com',
    description='A library for batch processing of data with custom conditions and processing functions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pedro_amad0/batch_processor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)