import logging

import ConfigParser
import urllib
import pycurl
import cStringIO
import re
import json
import time
import os.path

import browserHTTP


#########################################################################
class googleReaderError(Exception):    
    """Processing Error Exception stub """
 


########################################################################
class  googleReader(object):
    """ Simple interface for Google Reader
    see http://undoc.in/googlereader.html for complete documentation
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """ Constructor """
        self.myName = 'FeedFiddler'
        self.authFile = 'auth.txt'
        self.SessionToken = None
        
        self.apiURL = 'http://www.google.com/reader/api/0/'
        self.tokenURL = self.apiURL+'token'
        
        #read an initialization file that contains the values for the authentication tokens
        configs = ConfigParser.ConfigParser()
        configs.read('FeedFiddler.ini')
        
        #Password authentication method
        self.username = configs.get('SECURITY', 'username')
        self.password = configs.get('SECURITY', 'password')
        
        #Initialize the browser
        self.browser = browserHTTP.browserHTTP()
        
        
    #----------------------------------------------------------------------
    def authenticate(self):
        """Authenticate the reader connection
        
        This will check to see if a file exists with the contents of the authentiation token.
        If this file is not there, it will cause the login process to occur and the `result will be placed 
        in the newly created file.
        """
        
        if os.path.isfile(self.authFile):
            #grab the auth key in it
            authString = open(self.authFile, 'r').read()
        else:
            #Login to google and get the authentication key
            #create and store the key in the file
            authString = self.login()
            open(self.authFile, 'w').write(authString)
            
        #make it accessible for everyone else
        self.SessionToken = authString
        
    #----------------------------------------------------------------------
    def login(self):
        """Login to the service with your built in authentication method"""
        #This is will also register the security auth value, this is the openid session.
        #We are to hold on to this for the lifetime of the object.
        authString = None
        loginURL = 'https://www.google.com/accounts/ClientLogin'
        
        
        #create our string to look at curl's result later
        resultString = cStringIO.StringIO()
        
        #set the post data with what google reader expects us to have
        postData = { }
        
        postData['service'] = 'reader'
        postData['Email'] = self.username
        postData['Passwd'] = self.password
        postData['source'] = self.myName
        postData['continue'] = 'http://www.google.com'
        
        c = pycurl.Curl()
        c.setopt(c.URL, loginURL)
        c.setopt(c.POSTFIELDS, urllib.urlencode(postData))
        c.setopt(c.WRITEFUNCTION,  resultString.write)
        c.perform()
        idList = resultString.getvalue().split('\n')
        for elem in idList:
            isMatch = re.match('(\w*)(=)(.*)', elem)
            if isMatch:
                if isMatch.group(1) == 'Auth':
                    #register and STORE the session token
                    authString = isMatch.group(3)
                    break
        #raise an error condition if we are not able to find the Auth value
        if authString == None:
            raise googleReaderError('Invalid login: SessionToken was not generated')
        return authString
                
    #----------------------------------------------------------------------
    def getToken(self):
        """Get the token """
        self.browser.txHeaders = {}
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        return self.browser.get(self.tokenURL)
        
    #----------------------------------------------------------------------
    def getUserInfo(self):
        """Get the token """
        self.browser.txHeaders = {}
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        self.tokenURL = self.apiURL+'user-info'
        
        getParms = {}
        getParms['ck'] = int(time.time())
        getParms['application'] = self.myName
        return json.loads(self.browser.get(self.tokenURL))['userId']
        
    #----------------------------------------------------------------------
    def listFeeds(self):
        """List the feeds and return a list of subscriptions"""
        
        result = None
        subListURL = self.apiURL+'subscription/list?output=json'
        self.browser.postData = None
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        result = self.browser.get(subListURL)
        jsonResults = json.loads(result)
        result = jsonResults['subscriptions']
        return result
    #----------------------------------------------------------------------
    def listTags(self):
        """List the tags and return a list of tags"""
        
        result = None
        subListURL = self.apiURL+'tag/list?output=json'
        self.browser.postData = None
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        result = self.browser.get(subListURL)
        jsonResults = json.loads(result)
        result = jsonResults['tags']
        return result

    #----------------------------------------------------------------------
    def listArticles(self):
        """List all the articles"""
        result = None
        
        
        getParms = {}
        getParms['output'] = 'json'
        getParms['co'] = 'True'
        getParms['r'] = 'n'
        getParms['n'] = 10000
        getParms['ck'] = int(time.time())
        getParms['client'] = self.myName
        #exclude the items that have already been read
        getParms['xt'] = 'user/-/state/com.google/read'
        
        self.contentURL = self.apiURL+'stream/contents/user/-/state/com.google/' 
        
        subListURL = self.contentURL+'reading-list?%s' % urllib.urlencode(getParms)
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        result = self.browser.get(subListURL)
        jsonResults = json.loads(result)
        result = jsonResults['items']
        self.dumpResults(result, 'title')
        return result

    #----------------------------------------------------------------------
    def dumpResults(self, result, whichElement):
        fptr = open('dumpResults.txt','w')
        
        for elem in result:
            fptr.write(elem[whichElement].encode('ascii','ignore')+'\n')
    
    