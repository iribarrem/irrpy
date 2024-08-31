from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='irrpy',
    version='0.1.0',    
    description='Python module for retriving IP Prefixes from IRR Route Objects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iribarrem/irrpy/',
    author='Gustavo Iribarrem',
    author_email='gustavo.iribarrem@gmail.com',
    license='MIT',
    license_files = ('LICENSE.txt',),
    packages=['irrpy'],
    install_requires=['click'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
    ],
)