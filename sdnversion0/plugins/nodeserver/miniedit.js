var PythonShell = require('python-shell');
var http = require("http");
//var server = http.createServer

http.createServer(function (request, response) {

   // Send the HTTP header
   // HTTP Status: 200 : OK
   // Content Type: text/plain
 
    PythonShell.run('miniedit.py', function (err) {});

   
   response.writeHead(200, {'Content-Type': 'text/plain'});
  
   // Send the response body as "Hello World"
   response.end('Started Miniedit..\n');
}).listen(8081);

// Console will print the message
console.log('Server running at http://localhost:8081/');

