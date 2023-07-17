import os
import shutil
from get_filepaths import get_filepaths
import aiohttp
import asyncio
import ssl

sslcontext = ssl.create_default_context()

"""
Update the following lines if you get SSL cert errors, and if the fix
described at https://github.com/Rapptz/discord.py/issues/5968 doesn't work
"""
sslcontext.check_hostname = True
# sslcontext.check_hostname = False
sslcontext.verify_mode = ssl.CERT_REQUIRED
# sslcontext.verify_mode = ssl.CERT_NONE

async def download_file(session, url):
    # Get the filename by splitting on '/' and taking the last element
    filename = url.split("/")[-1]

    # Send a GET request
    async with session.get(url) as response:
        if response.status == 200:
            print(filename, "started...")
            # Write the contents of the response to a file in the output directory
            with open(os.path.join("output", filename), "wb") as file:
                total_downloaded = 0
                log_threshold = 10 * 1024 * 1024  # This is the threshold in bytes when we want to log.
                total_logged = 0
                chunk = await response.content.read(1024 * 1024)  # Setting chunk size to 1MB
                while chunk:
                    total_downloaded += len(chunk)
                    if total_downloaded - total_logged >= log_threshold:
                        print(f"{filename} downloading: {total_downloaded / (1024 * 1024)} MB")
                        total_logged = total_downloaded
                    file.write(chunk)
                    chunk = await response.content.read(1024 * 1024)
        else:
            print(f"Failed to download {url}")

async def download_files(urls):
    # Check if the output directory exists, if so, remove it
    if os.path.exists("output"):
        shutil.rmtree("output")

    # Recreate the output directory
    os.makedirs("output")

    # Create a ClientSession to manage our HTTP requests
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=sslcontext)) as session:
        # Use asyncio.gather to download files concurrently
        await asyncio.gather(*(download_file(session, url) for url in urls))

if __name__ == "__main__":
    urls = get_filepaths()
    asyncio.run(download_files(urls))
