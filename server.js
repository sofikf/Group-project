var express = require("express");
var path = require("path");

var app = express();
var port = 8080;

app.use((req, res, next) => {
    console.log("Incoming request:", req.method, req.url);
    next();
});

app.use(express.static(path.join(__dirname, "public")));

app.get("*name", function(req, res) { //comment ^4.21.1 to package.json:9     "express": "5.1.0" replace "expres": "^4.21.1"
    res.sendFile(path.join(__dirname, "public", "index.html"))
})

app.listen(port, function() {
    console.log("server on " + port);
})