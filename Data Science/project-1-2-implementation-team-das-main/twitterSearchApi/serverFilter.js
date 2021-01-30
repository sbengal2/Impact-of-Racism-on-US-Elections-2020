var express = require('express')
var app = express()
const url = "mongodb://localhost:27017/";
const needle = require('needle');

var scrapper = require('./scrapper').Scrapper;
var dataBaseConnection = require('./dataBaseConnection').DataBaseConnection;
var logger = require('./logger').Logger;

/**
 * this script is used to collect filter Sample stream
 */


var logger = new logger;
scrapper = new scrapper;
dataBaseConnection = new dataBaseConnection;

const user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld";
const media_fields="duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics";
const place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type";
const tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,source,text,withheld";
const poll_fields="duration_minutes,end_datetime,id,options,voting_status";
const rulesURL = 'https://api.twitter.com/2/tweets/search/stream/rules'

const urlOptions = {
    urlsampleSearch: "https://api.twitter.com/2/tweets/search/stream?tweet.fields="+tweet_fields+"&user.fields="+user_fields+"&place.fields="+place_fields+"&media.fields="+media_fields+"&poll.fields="+poll_fields,
    // darshan's twitter token
    tokenBearer: "Bearer AAAAAAAAAAAAAAAAAAAAAIebHAEAAAAA%2Bw85cBXqRDIEIgbWMH5gdm475DA%3DcGxKt0OmrbG2RKyx7uyNbesSj3zla5tiB9IzttuJShU24FIlf5"
};
var dataBase;

/**
 * defined rules for the filtered sample stream 
 */
const rules = [
    { "value": "(to:JoeBiden)(racism OR #WhatMatters2020 OR #blacklivesmatter OR #georgefloyd OR #nigeria OR #EndSarsNow)", "tag": "blackLivesMatterJoeSars" },
    { "value": "((@POTUS) (BlackLivesMatter OR Racism OR racism OR #WhatMatters2020 OR #blacklivesmatter OR #georgefloyd OR #nigeria OR #EndSarsNow) lang:en )", "tag": "blackLivesMattersPOTUS" },
    { "value": "((@realDonaldTrump) (BlackLivesMatter OR Racism OR racism OR #WhatMatters2020 OR #blacklivesmatter OR #georgefloyd OR #nigeria OR #EndSarsNow) lang:en )", "tag": "blackLivesMattersTrump" },
    { "value": "((to:POTUS OR to:realDonaldTrump) (racism OR #WhatMatters2020 OR #blacklivesmatter OR #georgefloyd OR #nigeria OR #EndSarsNow))", "tag": "blackLivesMatterTrumpSars" },
    { "value": "((BlackLivesMatter OR Racism OR racism OR #WhatMatters2020 OR #blacklivesmatter OR #georgefloyd OR #nigeria OR #EndSarsNow) (@JoeBiden) lang:en )", "tag": "blackLivesMatterJoe" },
    { "value": "((BlackLivesMatter OR Racism) (@JoeBiden) is:retweet lang:en )", "tag": "blackLivesMatterJoeRetweet" },
    { "value": "((BlackLivesMatter OR Racism) (@realDonaldTrump) is:retweet lang:en )", "tag": "blackLivesMatterTrumpRetweet" },
    { "value": "#ElectionDay OR #Election2020 OR GO VOTE OR #VoteBidenHarrisToSaveAmerica OR #Vote2020 OR #TRUMP2020Landside"}

];

async function getAllRules() {

    const response = await needle('get', rulesURL, {
        headers: {
            "authorization": urlOptions.tokenBearer
        }
    })

    if (response.statusCode !== 200) {
        throw new Error(response.body);
        return null;
    }

    return (response.body);
}

async function deleteAllRules(rules) {

    if (!Array.isArray(rules.data)) {
        return null;
    }

    const ids = rules.data.map(rule => rule.id);

    const data = {
        "delete": {
            "ids": ids
        }
    }

    const response = await needle('post', rulesURL, data, {
        headers: {
            "content-type": "application/json",
            "authorization": urlOptions.tokenBearer
        }
    })

    if (response.statusCode !== 200) {
        throw new Error(response.body);
        return null;
    }

    return (response.body);

}

async function setRules() {

    const data = {
        "add": rules
    }

    const response = await needle('post', rulesURL, data, {
        headers: {
            "content-type": "application/json",
            "authorization": urlOptions.tokenBearer
        }
    })

    if (response.statusCode !== 201) {
        throw new Error(response.body);
        return null;
    }

    return (response.body);

}

/**
 * streamConnect func used to create a needle request and put it to the database  
 */

function streamConnect() {
    const options = {
        timeout: 20000,
    }

    const stream = needle.get(urlOptions.urlsampleSearch, {
        headers: {
            Authorization: urlOptions.tokenBearer,
        }, options
    });

    stream.on('data', data => {
        try {
            const result = JSON.parse(data);
            dataBaseConnection.connectDataBase(url).then(function (db) {
                dataBase = db;
                dataBaseConnection.insertCollectionFilter(dataBase, result.data).then().catch(function (err) { console.log(err); logger.errorLogger(err); })
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

    // Listen to the stream.
    // This reconnection logic will attempt to reconnect when a disconnection is detected.
    // To avoid rate limites, this logic implements exponential backoff, so the wait time
    // will increase if the client cannot reconnect to the stream.
    // let currentRules;

     try {
         // Gets the complete list of rules currently applied to the stream
         currentRules = await getAllRules();

         // Delete all rules. Comment the line below if you want to keep your existing rules.
         await deleteAllRules(currentRules);

         // Add rules to the stream. Comment the line below if you don't want to add new rules.
         await setRules();

     } catch (e) {
         console.error(e);
         process.exit(-1);
     }


    const filteredSampledStream = streamConnect();
    let timeout = 0;
    filteredSampledStream.on('timeout', () => {
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
 * localhost:8082/close
 * will close the running  server Script
 */

app.get('/close', function (req, res) {
    console.log("ScrapperFilter Closed");
    res.send('hello world');
    process.exit();
});


/**
 * localhost:8082/test
 * will check for the server Script status where running or close
 */
app.get('/test', function (req, res) {
    console.log("ScrapperFilter is still alive");
    res.send('hello world');

});

app.listen(8082);
console.log('the serverFilter is started at port 8082');

/**
 * sample to get the request
 */
//curl https://api.twitter.com/2/tweets/sample/stream?q="media.fields" "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAIebHAEAAAAAvsZVkYwnFk4YGsx%2FnMw760DMrCU%3DNPoAFJ1guQmBFqi6oNFgronxqHfR0HdhCJX3pZNcwgvG4E7rVN""
