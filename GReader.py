import logging

import ConfigParser
import urllib
import pycurl
import cStringIO
import re
import json

import browserHTTP




########################################################################
class  grInterface(object):
    """ Simple interface for Google Reader"""
    #----------------------------------------------------------------------
    def __init__(self):
        """ Constructor """
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
                
    def getToken(self):
        """Get the token """
        self.browser.txHeaders = {}
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        return self.browser.get(self.tokenURL)
        
        
    def listFeeds(self):
        """List the feeds """
        
        subListURL = self.apiURL+'subscription/list?output=json'
        try:
            self.browser.postData = None
            self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
            result = self.browser.get(subListURL)
            jsonResults = json.loads(result)
            
            #print all the titles that we have subscriptions to
            for elem in jsonResults['subscriptions']:
                print elem['title']
                
            
        except browserHTTP.processingHTTPError, e:
            
            result = None
        x = 'foo'
        
    
    
    