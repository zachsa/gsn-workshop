import os
import shutil
from get_filepaths import get_filepaths
import aiohttp
import asyncio
import ssl

sslcontext = ssl.create_default_context()
sslcontext.check_hostname = True
sslcontext.verify_mode = ssl.CERT_REQUIRED

MAX_CONCURRENT = 4


async def download_file(session, url):
    filename = url.split("/")[-1]

    async with session.get(url) as response:
        if response.status == 200:
            print(filename, "started...")
            with open(os.path.join("output", filename), "wb") as file:
                total_downloaded = 0
                log_threshold = 10 * 1024 * 1024
                total_logged = 0
                chunk = await response.content.read(1024 * 1024)
                while chunk:
                    total_downloaded += len(chunk)
                    if total_downloaded - total_logged >= log_threshold:
                        print(
                            f"{filename} downloading: {total_downloaded / (1024 * 1024)} MB"
                        )
                        total_logged = total_downloaded
                    file.write(chunk)
                    chunk = await response.content.read(1024 * 1024)
        else:
            print(f"Failed to download {url}")


async def producer(queue, urls):
    for url in urls:
        # put the URL into the queue
        await queue.put(url)


async def consumer(queue, session):
    while True:
        # wait for an url from the producer
        url = await queue.get()
        # download the file
        await download_file(session, url)
        # Notify the queue that the item has been processed
        queue.task_done()


async def download_files(urls):
    if os.path.exists("output"):
        shutil.rmtree("output")

    os.makedirs("output")

    queue = asyncio.Queue()

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=sslcontext)
    ) as session:
        # start the producer task
        producer_task = asyncio.create_task(producer(queue, urls))
        # start consumer tasks
        consumer_tasks = [
            asyncio.create_task(consumer(queue, session)) for _ in range(MAX_CONCURRENT)
        ]

        # wait for the producer task to finish
        await producer_task

        # wait for the remaining tasks to be processed
        await queue.join()

        # cancel the consumer tasks
        for task in consumer_tasks:
            task.cancel()

        # wait for the consumer tasks to be cancelled
        await asyncio.gather(*consumer_tasks, return_exceptions=True)


if __name__ == "__main__":
    urls = get_filepaths()
    asyncio.run(download_files(urls))
