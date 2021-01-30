# project-1-2-implementation-team-das
project-1-2-implementation-team-das created by GitHub Classroom
Team Members:
Shashank
Darshan
Aravind

<br>
Twitter Sample  stream collection flow
<br>
Server.js  : 
<br>
1. Builds the URL using relevant data fields like media fields,user fields etc.
<br>
2. This URL is them  used to create a stream socket to accept data from twitter sampled stream 
<br>
3.The data is phrased and stored into the mongo data base.

From the directory twitterSearchApi 
<br>
run the command :
<br>
To run the 
<br>
go to the directory
<br>
npm install
<br>
npm run start 



Reddit collection flow
<br>
1. Search api is used to get all the relevant subreddits as per the query string
<br>
2. URL is built for each subreddit returned by the search api
<br>
3. Using the URL comments are fetched from each subreddit and stored into the data base.
<br>
To run:
<br>
From the directory reddit_scrapper run the command : "python3 trigger.py &”	
<br>
Note : note down the pid of the process after entering the command.
<br>
To stop the process: Run “kill -9 <pid>”

report folder contains project report
<br>