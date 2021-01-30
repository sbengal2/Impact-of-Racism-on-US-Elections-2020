var express = require('express')
var app = express()
const url = "mongodb://localhost:27017/";
const needle = require('needle');

var scrapper = require('./scrapper').Scrapper;
var dataBaseConnection = require('./dataBaseConnection').DataBaseConnection;
var logger = require('./logger').Logger;

/**
 * this script is used to collect Sample stream
 */

var logger = new logger;
scrapper = new scrapper;
dataBaseConnection = new dataBaseConnection;

/**
 * Field's used to append to url to extract the all the fields 
 */

const user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld";
const media_fields="duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics";
const place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type";
const tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,source,text,withheld";
const poll_fields="duration_minutes,end_datetime,id,options,voting_status";
const urlOptions = {
    urlsampleStream: "https://api.twitter.com/2/tweets/sample/stream?tweet.fields="+tweet_fields+"&user.fields="+user_fields+"&place.fields="+place_fields+"&media.fields="+media_fields+"&poll.fields="+poll_fields,
   //shashank's twitter token
    tokenBearer:"Bearer AAAAAAAAAAAAAAAAAAAAAKB8JAEAAAAAYJp%2F%2FADlmmX9KpSDcuwafG0kszk%3DfrgrIzxZ6ttUefkikU9mQ3RflOEG2mX5wTN7NeK61Qf57It285"
};
var dataBase;
/**
 * streamConnect func used to create a needle request and put it to the database  
 */

function streamConnect() {
    const options = {
        timeout: 20000,
    }

    const stream = needle.get(urlOptions.urlsampleStream, {
        headers: {
            Authorization: urlOptions.tokenBearer,
        }, options
    });

    stream.on('data', data => {
        try {
            const result = JSON.parse(data);
           // console.log(result);
            dataBaseConnection.connectDataBase(url).then(function (db) {
                dataBase = db;
                dataBaseConnection.insertCollection(dataBase, result.data).then().catch(function (err) { console.log(err); logger.errorLogger(err); })
            }).catch(function (err) { console.log(err); logger.errorLogger(err); });
          //  console.log(result);
        } catch (e) {
            // Keep alive signal received. Do nothing sss.
        }
    }).on('error', error => {
        if (error.code === 'ETIMEDOUT') {
            stream.emit('timeout');
        }
    });

    return stream;
};




(async () => {
    const sampledStream = streamConnect();
    let timeout = 0;
    sampledStream.on('timeout', () => {
        // Reconnect on error
        console.warn('A connection error occurred. Reconnecting…');
        setTimeout(() => {
            timeout++;
            streamConnect();
        }, 2 ** timeout);
        streamConnect();
    })

})();


/**
 * localhost:8080/close
 * will close the running  server Script
 */

app.get('/close', function (req, res) {
    console.log("Scrapper Closed");
    res.send('hello world');
    process.exit();
});


/**
 * localhost:8080/test
 * will check for the server Script status where running or close
 */

app.get('/test', function (req, res) {
    console.log("Scrapper is still alive");
    res.send('hello world');

});

app.listen(8080);
console.log('the server is started at port 8080');

/**
 * sample to get the request
 */
//curl https://api.twitter.com/2/tweets/sample/stream?q="media.fields" "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAIebHAEAAAAAvsZVkYwnFk4YGsx%2FnMw760DMrCU%3DNPoAFJ1guQmBFqi6oNFgronxqHfR0HdhCJX3pZNcwgvG4E7rVN""
