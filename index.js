const http = require('http')

function handle (req, res) {
  res.write('/path/to/file')
  res.end()
}

http.createServer(handle).listen(3000)