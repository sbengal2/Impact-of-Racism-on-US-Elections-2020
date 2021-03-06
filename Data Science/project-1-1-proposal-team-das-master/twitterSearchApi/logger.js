const fs = require('fs');
const fileName="logFile.txt";
class Logger {
    constructor() {
        this.createLoggerFile().then().catch(err => console.log("cannot create a logger file"));
    }

    createLoggerFile() {
        return new Promise(function (resolve, reject) {
            if (fs.existsSync(fileName)) {
                fs.appendFile(fileName, 'Server Started at ' + new Date()+"\r\n", function (err) {
                    if (err) reject(err);
                    resolve();
                });
            }
            else{
            fs.writeFile(fileName, 'Server Started at ' + new Date()+"\r\n", function (err) {
                if (err) reject(err);
                resolve();
            });
        }
        });
    }

    errorLogger(message) {
        return new Promise(function (resolve, reject) {
            fs.appendFile(fileName, message+"\r\n", function (err) {
                if (err) reject(err);
                resolve();
            });
        });
    }
}


module.exports.Logger = Logger;