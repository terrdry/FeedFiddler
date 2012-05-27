import logging

import ConfigParser
import urllib
import pycurl
import cStringIO
import re
import json
import time

import browserHTTP


#########################################################################
class googleReaderError(Exception):    
    """Processing Error Exception stub """
 


########################################################################
class  googleReader(object):
    """ Simple interface for Google Reader"""
    #----------------------------------------------------------------------
    def __init__(self):
        """ Constructor """
        self.myName = 'FeedFiddler'
        self.apiURL = 'http://www.google.com/reader/api/0/'
        self.tokenURL = self.apiURL+'token'
        self.loginURL = 'https://www.google.com/accounts/ClientLogin'
        
        #read an initialization file that contains the values for the authentication tokens
        configs = ConfigParser.ConfigParser()
        configs.read('FeedFiddler.ini')
        
        #Password authentication method
        self.username = configs.get('SECURITY', 'username')
        self.password = configs.get('SECURITY', 'password')
        
        #Initialize the browser
        self.browser = browserHTTP.browserHTTP()
        
        #session Token (Set to None before Login)
        self.SessionToken = None
        
    #----------------------------------------------------------------------
    def login(self):
        """Login to the service with your built in authentication method"""
        #This is will also register the security auth value, this is the openid session.
        #We are to hold on to this for the lifetime of the object.
        AUTHString = None
        
        #create our string to look at curl's result later
        resultString = cStringIO.StringIO()
        
        #set the post data with what google reader expects us to have
        postData = { }
        
        postData['service'] = 'reader'
        postData['Email'] = self.username
        postData['Passwd'] = self.password
        postData['source'] = 'terry'
        postData['continue'] = 'http://www.google.com'
        
        c = pycurl.Curl()
        c.setopt(c.URL, self.loginURL)
        c.setopt(c.POSTFIELDS, urllib.urlencode(postData))
        c.setopt(c.WRITEFUNCTION,  resultString.write)
        c.perform()
        idList = resultString.getvalue().split('\n')
        for elem in idList:
            isMatch = re.match('(\w*)(=)(.*)', elem)
            if isMatch:
                if isMatch.group(1) == 'Auth':
                    #register and STORE the session token
                    self.SessionToken = isMatch.group(3)
                    break
        #raise an error condition if we are not able to find the Auth value
        if self.SessionToken == None:
            raise googleReaderError('Invalid login: SessionToken was not generated')
                
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
        getParms['n'] = 500
        getParms['ck'] = int(time.time())
        getParms['client'] = self.myName
        self.contentURL = self.apiURL+'stream/contents/user/%s/state/com.google/' % self.getUserInfo()
        
        subListURL = self.contentURL+'reading-list?%s' % urllib.urlencode(getParms)
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        result = self.browser.get(subListURL)
        jsonResults = json.loads(result)
        result = jsonResults['items']
        for elem in result:
            print elem['title']
        return result
    
    