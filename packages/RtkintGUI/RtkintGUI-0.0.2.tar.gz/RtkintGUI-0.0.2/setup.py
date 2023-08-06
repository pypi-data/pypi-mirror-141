from unicodedata import name
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'RtkintGUI',
    version = '0.0.2',
    description='Sipmle GUI',
    long_description= long_description,
    long_description_content_type="text/markdown",
    url= '',
    author= 'Rana Anter',
    author_email='ranaanter919@gmail.com',
    license='MIT',
    classifiers= classifiers,
    keywords='GUI',
    packages=find_packages(),
    install_requires =['']
)