const http = require('http');
const os = require('os');
const server = http.createServer((req,res)=>{
    console.log(`Received request for URL ${req.url} using method ${req.method}`);
    res.writeHead(200,{'Content-Type':'text/plain'});
    const response = 'Hello world, '+ os.arch() + ' '+os.platform() + ' '+os.homedir();
    res.end(response);

});

server.listen(3000, ()=>{
    console.log("server successfully running");
})