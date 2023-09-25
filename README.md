**Readme.md**

**Python utility to download a zip archive from a link, extract it to temporary storage, and upload the extracted files to an S3 bucket.**

**Usage:**

```
s3_zip_uploader_cli <link to zip archive>
```

**Example:**

```
s3_zip_uploader_cli https://example.com/archive.zip
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

***Installation:***

**Create a virtual environment**

```
python3.9 -m venv venv
```

This will create a new Python environment that is isolated from your system Python environment. This is useful for avoiding conflicts with other Python packages that you may have installed.

**Activate the virtual environment**
```
source venv/bin/activate
```
This will activate the virtual environment. Once the virtual environment is activated, all Python commands will be run using the Python installation in the virtual environment.

**Install the required Python packages**
```
pip install -r requirements.txt
```
This will install all the Python packages that are required by your project. The `requirements.txt` file is a list of all the Python packages that your project needs, along with their versions.

**Build the project**
```
python setup.py sdist bdist_wheel
```
This will build your project into a distribution package. The distribution package can be installed on other systems using the pip install command.

**Install the project**

```
pip install .
```
This will install your project inside the virtual environment.

**AWS credentials:**

This script uses your AWS credentials to connect to S3. You can provide your credentials in a `.env` file, or you can enter them interactively when prompted.

To create a `.env` file, add the following lines to a text file named `.env`:

```
AWS_ACCESS_KEY_ID=<your AWS access key ID>
AWS_SECRET_ACCESS_KEY=<your AWS secret access key>
```

Then, place the `.env` file in the same directory as this script.

**Running:**

```
s3_zip_uploader_cli <link to zip archive>
```

**Troubleshooting:**

If you are having problems running the script, please check the following:

* Make sure that you have installed all of the required dependencies.
* Make sure that you have provided your AWS credentials.
* Make sure that the link to the zip archive is valid.
* Make sure that you have permission to write to the S3 bucket.

If you are still having problems, please open an issue on GitHub.