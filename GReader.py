import logging

import ConfigParser
import urllib
import pycurl
import cStringIO
import re



########################################################################
class  grInterface(object):
    """ Simple interface for Google Reader"""
    #----------------------------------------------------------------------
    def __init__(self):
        """ Constructor """
        self.baseURL = 'http://www.google.com/reader'
        self.loginURL = 'https://www.google.com/accounts/ClientLogin'
        
        #read an initialization file that contains the values for the authentication tokens
        configs = ConfigParser.ConfigParser()
        configs.read('FeedFiddler.ini')
        
        #Password authentication method
        self.username = configs.get('SECURITY', 'username')
        self.password = configs.get('SECURITY', 'password')
        
    def login(self):
        """Login to the service with your built in authentication method"""
        SIDString = None
        
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
            isMatch = re.match('(SID=)(.*)', elem)
            if isMatch:
                SIDString =  isMatch.group(2)
                break
            
        return SIDString
            
        
    
    
    