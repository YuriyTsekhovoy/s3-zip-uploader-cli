import argparse
import concurrent.futures
import logging
import boto3

def upload_file_to_s3(s3_client, bucket_name, object_key, file_path):
    """Uploads a file to S3.

    Args:
        s3_client: A boto3 S3 client.
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object in S3.
        file_path: The path to the file to upload.
    """

    with open(file_path, "rb") as f:
        s3_client.upload_fileobj(f, bucket_name, object_key)

def upload_zip_archive_to_s3(s3_client, bucket_name, zip_archive_url, concurrency):
    """Uploads a ZIP archive to S3 with concurrency.

    Args:
        s3_client: A boto3 S3 client.
        bucket_name: The name of the S3 bucket.
        zip_archive_url: The URL of the ZIP archive.
        concurrency: The number of concurrent uploads.
    """

    logging.info("Downloading ZIP archive from %s", zip_archive_url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for file_path in extract_zip_archive(zip_archive_url):
            future = executor.submit(upload_file_to_s3, s3_client, bucket_name, file_path, file_path)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            future.result()

def extract_zip_archive(zip_archive_url):
    """Extracts a ZIP archive.

    Args:
        zip_archive_url: The URL of the ZIP archive.

    Returns:
        A list of the paths to the extracted files.
    """

    import requests
    import zipfile

    logging.info("Extracting ZIP archive")
    response = requests.get(zip_archive_url)
    with zipfile.ZipFile(response.content) as zip_file:
        zip_file.extractall()

    return zip_file.namelist()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip-archive-url", required=True, help="The URL of the ZIP archive to upload.")
    parser.add_argument("--bucket-name", required=True, help="The name of the S3 bucket to upload the files to.")
    parser.add_argument("--concurrency", type=int, default=10, help="The number of concurrent uploads.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)

    s3_client = boto3.client("s3")

    upload_zip_archive_to_s3(s3_client, args.bucket_name, args.zip_archive_url, args.concurrency)

if __name__ == "__main__":
    main()
