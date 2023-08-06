import setuptools

import myacme
import myacme.__main__

setuptools.setup(
    name         = 'myacme',
    version      = myacme.__version__,
    author       = 'AXY',
    author_email = 'axy@declassed.art',
    description  = 'MyACME client library and command line tool',

    long_description = myacme.client.__doc__ + '\n\n' + myacme.__main__.__doc__,
    long_description_content_type = 'text/x-rst',

    url = 'https://declassed.art/repository/myacme',

    packages = ['myacme'],

    entry_points = {
        'console_scripts': [
            'myacme=myacme.__main__:main'
        ]
    },

    install_requires=[
        'idna',
        'kvgargs',
        'requests',
        'cryptography>=3.1'
    ],

    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha'
    ],

    python_requires = '>=3.6',
)
