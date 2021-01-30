
var MongoClient = require('mongodb').MongoClient;
var counter = 0;
class DataBaseConnection {
    constructor() {
        counter = 0;
    }

    connectDataBase(url) {
        return new Promise((resolve, reject) => {
            MongoClient.connect(url, { useUnifiedTopology: true }, function (err, db) {
                err
                    ? reject(err)
                    : resolve(db);
            });
        });
    }
    insertCollection(dbIn, myObj) {
        return new Promise((resolve, reject) => {
            var dbo = dbIn.db("myDb");
            dbo.collection("twitterDataSampleAll").insertOne(myObj, function (err, res) {
                if (err) reject(err);
                counter++;
               // console.log(counter + " " + " document inserted");
                dbIn.close();
                resolve();
            });
        })
    }
    insertCollectionFilter(dbIn, myObj) {
        return new Promise((resolve, reject) => {
            var dbo = dbIn.db("myDb");
            dbo.collection("twitterDataAllFilter").insertOne(myObj, function (err, res) {
                if (err) reject(err);
                counter++;
               // console.log(counter + " " + " document inserted");
                dbIn.close();
                resolve();
            });
        })
    }


}



module.exports.DataBaseConnection = DataBaseConnection;