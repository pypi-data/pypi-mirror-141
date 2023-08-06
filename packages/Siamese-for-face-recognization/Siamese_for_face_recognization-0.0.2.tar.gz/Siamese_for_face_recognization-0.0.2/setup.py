#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
	]

setup(
    name='Siamese_for_face_recognization',
    version='0.0.2',
    description="Models used for face_recognition by siamese neural network.",
    long_description=readme,
	long_description_content_type="text/markdown",
    author="AlphonseInbarajXavier",
    author_email='xalphonse@gmail.com',
    url='https://github.com/xalphonseinbaraj/Siamese_for_face_recognization',
    packages=[
        'Siamese_for_face_recognization',
    ],
    package_dir={'Siamese_for_face_recognization': 'Siamese_for_face_recognization'},
    package_data={
        'Siamese_for_face_recognization': ['models/*.dat'],
		'Siamese_for_face_recognization': ['models/*.xml'],
		'Siamese_for_face_recognization': ['models/*.h5'],
		
    },
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='Siamese_for_face_recognization',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],

)
