'''
Flask-Pourer
------------
Flask-Pourer is an extension for Flask that adds support for JSONAPI with Mongodb to your application.
'''
from setuptools import setup

setup(
    name='Flask-Pourer',
    version='0.0.1',
    url='https://github.com/pythonistas-tw/flask_pourer',
    license='MIT',
    author='Pythonistas Taiwan',
    author_email='contact@pythonistas.tw',
    description='Extension of JSONAPI for flask',
    long_description=__doc__,
    py_modules=['flask_pourer'],
    packages=['flask_pourer'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'pymongo',
        'python-mimeparse'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
