import os
import tempfile
import unittest
import zipfile

import boto3
import moto

from s3_zip_uploader_cli import (download_zip_archive, extract_zip_archive,
                                 create_s3_connection, create_s3_bucket,
                                 list_all_file_paths, upload_files_to_s3)


class TestS3ZipUploader(unittest.TestCase):

    def test_download_zip_archive(self):
        """Tests the download_zip_archive() function."""

        # Mock the requests library so that we can return a mock response.
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b'This is the content of the zip archive.'

        with unittest.mock.patch('requests.get', return_value=mock_response):
            # Download the zip archive to a temporary file.
            temp_zip_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
            download_zip_archive('https://example.com/my_zip_archive.zip', temp_zip_file.name)

            # Verify that the zip archive was downloaded successfully.
            self.assertEqual(temp_zip_file.read(), b'This is the content of the zip archive.')

            # Close the temporary zip file.
            temp_zip_file.close()

    def test_extract_zip_archive(self):
        """Tests the extract_zip_archive() function."""

        # Create a temporary zip file.
        temp_zip_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
        with zipfile.ZipFile(temp_zip_file.name, 'w') as zip_file:
            zip_file.write('requirements.txt')

        # Extract the zip archive to a temporary directory.
        temp_dir = extract_zip_archive(temp_zip_file.name)

        # Verify that the file was extracted successfully.
        self.assertTrue(os.path.exists(os.path.join(temp_dir, 'requirements.txt')))

        # Close the temporary zip file.
        temp_zip_file.close()

    @moto.mock_s3()
    def test_create_s3_connection(self):
        """Tests the create_s3_connection() function."""

        # Create an S3 connection.
        s3_connection = create_s3_connection()

        # Verify that the connection is valid.
        self.assertIsNotNone(s3_connection)

    @moto.mock_s3()
    def test_create_s3_bucket(self):
        """Tests the create_s3_bucket() function."""

        # Create an S3 client object.
        s3_connection = boto3.client('s3')

        # Create an S3 bucket.
        bucket_name = create_s3_bucket(s3_connection)

        # Verify that the bucket was created successfully.
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(bucket_name)
        exists = s3_resource.meta.client.head_bucket(Bucket=bucket.name)

        self.assertTrue(exists)

    def test_list_all_file_paths_with_subdirectories(self):
        """Tests the list_all_file_paths() function with subdirectories."""

        # Create a temporary directory.
        temp_dir = tempfile.mkdtemp()

        # Create a subdirectory.
        subdirectory = os.path.join(temp_dir, 'subdir')
        os.mkdir(subdirectory)

        # Create a file in the subdirectory.
        with open(os.path.join(subdirectory, 'my_file.txt'), 'w') as f:
            f.write('This is the content of my file.')

        # Get a list of all file paths in the directory.
        file_paths = list_all_file_paths(temp_dir)

        # Verify that the list contains the file path to the file in the subdirectory.
        self.assertIn(os.path.join(subdirectory, 'my_file.txt'), file_paths)

    @moto.mock_s3()
    def test_upload_files_to_s3(self):
        """Tests the upload_files_to_s3() function."""

        # Create an S3 client object.
        s3_connection = boto3.client('s3')

        # Create an S3 bucket.
        s3_bucket_name = create_s3_bucket(s3_connection)

        # Upload a file to the S3 bucket.
        upload_files_to_s3('requirements.txt', s3_bucket_name, 'requirements.txt')

        # Verify that the file was uploaded successfully.
        s3_client = boto3.client('s3')
        object_exists = s3_client.head_object(Bucket=s3_bucket_name, Key='requirements.txt')

        self.assertTrue(object_exists)
