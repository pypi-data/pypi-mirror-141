from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3'
]

setup(name='FibonacciGenerator', 
        version='0.1.2', 
        description='A python package for calculating fibonacci numbers', 
        long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
        url='', 
        author='Snehan Biswas',
        author_email = 'snehanb24118836@gmail.com',
        license='MIT',
        classifiers=classifiers,
        keywords='',
        packages=['FibonacciGenerator'], 
        install_requires=['numpy'])