const express = require('express');
PORT = 8081;

const logger = require('morgan');
const app = express();
const KML = require('jade').compileFile(__dirname + '/source/templates/KMLApps.jade');
const bodyParser = require('body-parser');

app.use(logger('dev'));
app.use(express.static(__dirname + '/static'));
app.use(bodyParser.json({ type: 'application/*+json' }));

/* Site directory */

app.get('/', function (req, res, next) {
    try {
        var html = KML({ title: 'KMLApps' });
        res.send(html);
    } catch (e) {
        next(e)
    }
});

/* Listen on port */

app.listen(process.env.PORT || 4000, function(){
  console.log('Your node js server is running');
});
