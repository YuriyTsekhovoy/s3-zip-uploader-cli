**Readme.md**

**Python utility to download a zip archive from a link, extract it to temporary storage, and upload the extracted files to an S3 bucket.**

**Usage:**

```
python upload_files_to_s3.py <link to zip archive>
```

**Example:**

```
python upload_files_to_s3.py https://example.com/archive.zip
```

This script will:

1. Download the zip archive from the specified link.
2. Extract the zip archive to temporary storage.
3. Create an S3 bucket if one does not already exist.
4. Upload the extracted files to the S3 bucket.
5. Delete the local zip file and extracted files.

**Requirements:**

* Python 3
* boto3
* requests
* environs

**Installation:**

```
pip install -r requirements.txt
```

**Running:**

```
python upload_files_to_s3.py <link to zip archive>
```

**AWS credentials:**

This script uses your AWS credentials to connect to S3. You can provide your credentials in a `.env` file, or you can enter them interactively when prompted.

To create a `.env` file, add the following lines to a text file named `.env`:

```
AWS_ACCESS_KEY_ID=<your AWS access key ID>
AWS_SECRET_ACCESS_KEY=<your AWS secret access key>
```

Then, place the `.env` file in the same directory as this script.

**Troubleshooting:**

If you are having problems running the script, please check the following:

* Make sure that you have installed all of the required dependencies.
* Make sure that you have provided your AWS credentials.
* Make sure that the link to the zip archive is valid.
* Make sure that you have permission to write to the S3 bucket.

If you are still having problems, please open an issue on GitHub.