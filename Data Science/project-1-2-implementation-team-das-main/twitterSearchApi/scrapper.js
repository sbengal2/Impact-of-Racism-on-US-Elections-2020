var express = require('express')
var app = express()
var request = require('request')
const fs = require('fs');
const needle = require('needle');
/**
 * Used to filter the data and maps it  required field
 */
class Scrapper {


    constructor() {

    }

    async responseFilter(data) {
        return await new Promise(function (resolve, reject) {
            let returnData = { twitterData: [] };
            data.map(function (a) {
                let twData = {
                    "created_at": a.created_at,
                    "id": a.id_str,
                    "text": a.text,
                    "geo": a.geo,
                    "coordinates": a.coordinates,
                    "place": a.place,
                    "retweeted_status": a.retweeted_status,
                    "entities":a.entities
                }
                returnData.twitterData.push(twData);
            });
            resolve(returnData);
        });
    }


    

    loadApiData() {
        return new Promise((resolve, reject) => {
            fs.readFile('constApiData/apiData.json', (err, data) => {
                err
                    ? reject(err)
                    : resolve(JSON.parse(data));
            });
        });
    };


    requestPromise(urlOptions) {
        var self = this;
        return new Promise(function (resolve, reject) {
            console.log(urlOptions.twitterApiData[0].urlApiSearch);
            request({
                url: urlOptions.twitterApiData[0].urlApiSearch,
                headers: {
                    'Authorization': urlOptions.twitterApiData[0].bearerToken
                },
                rejectUnauthorized: false
            }, function (err, res, body) {
                if (err) {
                    reject("request failed");
                }
                else {
                    if (JSON.parse(body).errors != undefined) {
                        reject(body);
                    }
                    else {
                        body = JSON.parse(body);
                       // console.log(body);
                        self.responseFilter(body.statuses).then(function (result) {
                            // console.log(result);
                            console.log("It was a success.");
                            resolve(result)
                        });
                    }
                }
            }
            )
        })
    };
}



module.exports.Scrapper = Scrapper;
