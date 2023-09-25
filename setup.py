#!/usr/bin/env python

from setuptools import setup

setup(
    name='s3_zip_uploader_cli',
    version='0.1.0',
    description='Downloads a zip archive from a link, extracts it to temporary storage, and uploads the extracted files to S3.',
    author='YuriyTsekhovoy',
    author_email='yuriy.tsekhovoy@google.com',
    url='https://github.com/YuriyTsekhovoy/s3-zip-uploader-cli',
    install_requires=[
        'boto3',
        'environs',
        'moto',
    ],
    entry_points={
        'console_scripts': [
            's3_zip_uploader_cli = s3_zip_uploader_cli:main',
        ],
    },
)
