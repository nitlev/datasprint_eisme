# Data Sprint EISME
![travis-CI](https://travis-ci.org/nitlev/datasprint_eisme.svg?branch=master)

This is supposed to be a simple bot, helping people getting information from 
organized public data.


# BBL DAY (24/01/2017)
Today we share this code along with some other apps to our folks at OCTO. 
Let's see if they can fix it ;-)

# D-DAY ! (6/12/2016)
This is it guys ! The hackathon is now live.

Right now (9pm UTC+1) the bot runs with a simple interface.
The workflow is currently following this path :
* The users sends a message in the web interface
* A javascript script sends to an endpoint the message, which is then passed 
to the server.
* The server sends back the message to be displayed on the web interface, and 
sends it to the Wit.ai API
* The server gets back the analysis from Wit.ai
* The server uses this analysis to build a query, and sends this query to our 
search API
* The search API responds with a list of documents/urls
* The servers sends to the web app a couple of messages to be sent to the user,
 using the url of the documents.
* The user can use the links to display the documents, and make sure the 
document match their interest 
