
var MongoClient = require('mongodb').MongoClient;
var counter = 0;

/*
  Class used to Connect the data base
*/
class DataBaseConnection {
    constructor() {
        counter = 0;
    }

    /**
     * Methood used to connect to dataBase
     * @param {*} url  
     */
    connectDataBase(url) {
        return new Promise((resolve, reject) => {
            MongoClient.connect(url, { useUnifiedTopology: true }, function (err, db) {
                err
                    ? reject(err)
                    : resolve(db);
            });
        });
    }
    /**
     * Method used to insert to dataBase for data Stream
     * @param {*} dbIn  database obj
     * @param {*} myObj 
     */
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
    /**
     * 
     * Method used to insert to dataBase used for Filter data Stream
     * @param {*} dbIn 
     * @param {*} myObj 
     */
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