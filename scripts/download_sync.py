import os
import shutil
import requests
import json

def get_filepaths():
    url = "https://mnemosyne.somisana.ac.za/somisana/algoa-bay/5-day-forecast/202307"
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    forecast = []
    for item in data:
        if 'entry' in item and item['entry'].endswith("-t3.nc"):
            forecast.append("https://mnemosyne.somisana.ac.za" + item['path'])

    return forecast


def download_files(urls):
    # Check if the output directory exists, if so, remove it
    if os.path.exists("output"):
        shutil.rmtree("output")

    # Recreate the output directory
    os.makedirs("output")

    # Iterate over the list of URLs
    for url in urls:
        # Get the filename by splitting on '/' and taking the last element
        filename = url.split("/")[-1]

        # Send a GET request
        response = requests.get(url, stream=True)

        # Check that the GET request was successful
        if response.status_code == 200:
            print(filename, "started...")
            # Write the contents of the response to a file in the output directory
            with open(os.path.join("output", filename), "wb") as file:
                chunk_size = 1024 * 1024  # Setting chunk size to 1MB
                total_downloaded = 0
                log_threshold = 10  # This is the threshold in MB when we want to log. Change as per your requirement.
                total_logged = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    total_downloaded += len(
                        chunk
                    )  # We use len(chunk) instead of chunk_size because the last chunk might be smaller than chunk_size.
                    downloaded_mb = total_downloaded / (1024 * 1024)
                    if downloaded_mb - total_logged >= log_threshold:
                        print(f"{filename} downloading: {downloaded_mb} MB")
                        total_logged = downloaded_mb
                    file.write(chunk)
        else:
            print(f"Failed to download {url}")


if __name__ == "__main__":
    urls = get_filepaths()
    download_files(urls)
