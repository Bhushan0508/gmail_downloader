import gdown

url = 'https://drive.google.com/uc?id=1MY4SSSEE-DL17ecWmjh5cNWKq2MxN7I8'  # Replace with the file URL
output = 'downloaded_file.ext'  # Replace with desired filename
gdown.download(url, output, quiet=False)  # Set quiet=True to suppress progress