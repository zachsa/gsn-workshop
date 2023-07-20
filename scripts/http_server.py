from aiohttp import web
import aiofiles

# Layer 4 - Transport layer is responsible for end-to-end communication over a network. 
# This includes definition of the protocol port numbers. 
# Python's aiohttp library abstracts away the details of the transport layer (like TCP), 
# but it is handled by the underlying asyncio and socket libraries in Python.
PORT = 8080

async def file_download(request):
    # The application layer in the TCP/IP model corresponds to the application, presentation, 
    # and session layers in the OSI model.
    # Layer 7 - Application layer (TCP/IP model) 
    filename = request.match_info.get('filename', "test.txt")

    # Open file in a non-blocking way
    async with aiofiles.open(filename, 'rb') as f:
        # Stream file back to client without loading it all into memory
        response = web.StreamResponse()

        # Prepare response headers
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        await response.prepare(request)

        # Read file by chunks and write to response while there's data left to read
        chunk = await f.read(1024)
        while chunk:
            await response.write(chunk)
            chunk = await f.read(1024)

        return response

app = web.Application()
app.router.add_get('/download/{filename}', file_download)

# The underlying asyncio and socket libraries handle the transport layer (TCP/IP)
web.run_app(app, port=PORT)
