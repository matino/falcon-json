from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='falcon_json',
    author='Mateusz Czubak',
    author_email='mczubak@gmail.com',
    url='https://github.com/matino/falcon-json',
    version='0.0.1',
    classifiers=classifiers,
    description='Falcon JSON helpers',
    long_description=open('README.md').read(),
    keywords='falcon json api',
    packages=find_packages(include=('falcon_json*',)),
    install_requires=open('requirements.txt').read(),
    include_package_data=True,
    license='Apache License 2.0',
)
