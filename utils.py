import logging
import os
import sys
import tempfile
import requests

# Define the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler and add it to the logger
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Define a function to download a zip archive from a link
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

# Define a function to main function
def main():
    """Downloads a zip archive from a link and saves it to a temporary file.

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
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    # Close the temporary file
    temp_zip_file.close()

    # Print the path to the temporary file
    print(temp_zip_file.name)

# Call the main function if this script is being run directly
if __name__ == '__main__':
    main()
