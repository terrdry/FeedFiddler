FeedFiddler
===========

Utility for reading Google Reader RSS feeds and tagging articles

A configuration file is read and a list of regular expressions are used
to scan through all the unread articles in your GoogleReader feeds. Once 
a hit is acquired on an unread article, it is tagged with the regular 
expression's tag string. If a tag doesn't already exist, it will be created 
and the article will be linked to it. 

The application will use the security credentials in the initialization file
to login to the Google account of the user. An auth.txt file will be created 
that will contain an authorization key from Google. As long as the file exists 
the authorization key will be used to authenticate and create a connection to 
Google. Deleting the auth.txt file will cause the auth key to be regenerated 
with an additional login to Google.

All runs are tracked in a log file that is generated by the application. This
can be used for debugging.


Prerequisites
-------------

pyCurl
GoogleReader account

Setup
-----
Update the FeedFiddler.ini file

    [SECURITY]
    username=<userName>@gmail.com
    password=********
    
Create your regex expression and the corresponding tag that the article will appear under

    [RULES]
    programming=Python|Ruby
    programming=C|Haskell
    dvcs=git\b|mercurial\b|github\b|bitbucket\b

You can have multiple entries for the same tag with different regular expressions

Usage
-----

You can just invoke it from the command line,

    ./FeedFiddler.py
    
Or, put it in a cron job and forget about it.

