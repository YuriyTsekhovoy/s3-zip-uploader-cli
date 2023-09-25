import logging
import os
import shutil
import sys
import tempfile
import threading
import uuid
import zipfile

import boto3
import requests
from environs import Env

env = Env()
env.read_env()

# Getting AWS credentials from .env variable
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and add it to the logger
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def download_zip_archive(link, temp_zip_file):
    """Downloads a zip archive from a link and saves it to a temporary file.

    Args:
        link (str): The link to the zip archive.
        temp_zip_file (str): The path to the temporary file to save the zip archive to.

    Returns:
        None
    """

    logger.info('Downloading zip archive from link: {}'.format(link))

    response = requests.get(link)
    if response.status_code != 200:
        raise Exception('Failed to download zip archive: {}. Status code: {}'.format(link, response.status_code))

    with open(temp_zip_file, 'wb') as f:
        f.write(response.content)

    logger.info('Zip archive downloaded successfully.')


def extract_zip_archive(temp_zip_file):
    """Extracts a zip archive to temporary storage.

    Args:
        temp_zip_file (str): The path to the temporary zip archive to extract.

    Returns:
        str: The path to the temporary directory containing the extracted files.
    """

    logger.info('Extracting zip archive: {}'.format(temp_zip_file))

    temp_dir = tempfile.mkdtemp()

    with zipfile.ZipFile(temp_zip_file, 'r') as zip_file:
        zip_file.extractall(temp_dir)

    logger.info('Zip archive extracted successfully.')

    return temp_dir


def create_s3_connection():
    """Creates an S3 connection.

    Returns:
        An S3 connection object.
    """

    logger.info('Creating S3 connection')

    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                 )
    s3_connection = s3_resource.meta.client

    logger.info('S3 connection created successfully.')

    return s3_connection


def create_s3_bucket(s3_connection):
    """Creates an S3 bucket.

    Args:
        s3_connection: An S3 client object.

    Returns:
        None
    """

    bucket_prefix = 'extracted-zip'
    bucket_name = '-'.join([bucket_prefix, str(uuid.uuid4())])
    logger.info('Creating S3 bucket: {}'.format(bucket_name))
    try:
        session = boto3.session.Session()
        current_region = session.region_name
        s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': current_region})
        return bucket_name
    except Exception as e:
        raise Exception('Failed to create S3 bucket: {}'.format(e))

    logger.info('S3 bucket created successfully.')


def list_all_file_paths(directory):
    """Lists all file paths in a directory tree.
    Args:
        directory: The directory to list.
    Returns:
        A list of all file paths in the directory tree.
    """
    logger.info('Listing all file paths in: {}'.format(directory))

    file_paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def upload_files_to_s3(local_file_path, s3_bucket_name, s3_key):
    """Uploading files from temporary storage to S3 bucket"""
    logger.info('Upload {} file to S3 bucket: {}'.format(local_file_path, s3_bucket_name))

    s3 = boto3.client('s3')
    try:
        s3.upload_file(Filename=local_file_path, Bucket=s3_bucket_name, Key=s3_key)

    except (IsADirectoryError, FileNotFoundError) as e:
        raise Exception('Failed to upload file to S3 bucket: {}'.format(e))

    logger.info('{} file uploaded successfully to S3 bucket: {}'.format(s3_key, s3_bucket_name))


def main():
    """Downloads a zip archive from a link and extracts it to temporary storage.

    Returns:
        None
    """

    # Get the link to the zip archive from the command line arguments
    link = sys.argv[1]

    # Create a temporary file to save the zip archive to
    temp_zip_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)

    try:
        # Download the zip archive
        download_zip_archive(link, temp_zip_file.name)

        # Extract the zip archive to temporary storage
        temp_dir = extract_zip_archive(temp_zip_file.name)

        logger.info('Files extracted to {}'.format(temp_dir))

        # Create s3 connection
        s3_connection = create_s3_connection()

        # Create s3 bucket
        s3_bucket_name = create_s3_bucket(s3_connection)

        # List file paths
        file_paths = list_all_file_paths(temp_dir)

        # Upload files from local dir to s3 bucket
        threads = []
        for file in file_paths:
            s3_file = file.split(temp_dir)[1]
            thread = threading.Thread(target=upload_files_to_s3, args=(file, s3_bucket_name, s3_file))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Delete the local zip file and extracted files
        os.remove(temp_zip_file.name)
        shutil.rmtree(temp_dir)
        logger.info('Local zip file and extracted files have been deleted')


    except Exception as e:
        logger.error(e)
        sys.exit(1)

    # Close the temporary zip file
    temp_zip_file.close()


# Call the main function if this script is being run directly
if __name__ == '__main__':
    main()
