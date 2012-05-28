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

logger = logging.getLogger('ff.%s' % __name__)
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
        
        # a list of tuples composed of  a tag and its regular expression 
        self.rules= configs.items('RULES')
        
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
            logger.info('Used the auth file for authentication')
            authString = open(self.authFile, 'r').read()
        else:
            #Login to google and get the authentication key
            #create and store the key in the file
            logger.info('Logging in to Google for authentication')
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
            errorMessage = 'Invalid login: SessionToken was not generated'
            logger.error(errorMessage)
            raise googleReaderError(errorMessage)
        
        return authString
                
    #----------------------------------------------------------------------
    def getToken(self):
        """Get the token """
        logger.info('Token being retrieved...')
        self.browser.txHeaders = {}
        self.browser.txHeaders['authorization']= 'GoogleLogin auth=%s' % self.SessionToken
        return self.browser.get(self.tokenURL)
        
    #----------------------------------------------------------------------
    def getUserInfo(self):
        """Get the token """
        logger.info('UserInfo being retrieved...')
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
        
        #list results for debugging 
        [ logger.debug('feed item: %s' % self.sanitize(element['title']) ) for element in result]
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
        
        #list results for debugging 
        [ logger.debug('tag item: %s' % self.sanitize(element['id']) ) for element in result]
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
        #list results for debugging 
        [ logger.debug('article item: %s' % self.sanitize(element['title']) ) for element in result]
        return result

    #----------------------------------------------------------------------
    def listAndTagArticles(self):
        """List unread articles and implement search and tagging"""
        result = False
        
        #theURL for edititing our articles
        editTagURL = self.apiURL+'edit-tag'
        
        #define the list of fields we may want to search
        lookList = [ 'elem["title"]', \
                     'elem["content"]["content"]',
                     'elem["summary"]["content"]' ]
        
        #Get the token that will be used for all subsequent transactions 
        transactionToken = self.getToken()
        
        #optimize the variable lookup
        urlEncode = browserHTTP.urlEncode
        
                    
        logger.info('List and tag articles')
        for elem in self.listArticles():
            searchTarget = ''
            for i in lookList:
                try:
                    searchTarget += self.sanitize(eval(i))
                except KeyError:
                    pass
                
            logger.debug('search target is %s' % searchTarget)
            for regex in self.rules:
                if re.search(regex[1], searchTarget):
                
                    postParms={}
                    postParms['T'] = transactionToken
                    postParms['a'] = 'user/-/label/%s'  % regex[0]
                    postParms['i'] = elem['id']
                    postParms['s'] = elem['origin']['streamId']
                    postParms['asynch'] = 'true'
                    pParms = urlEncode(postParms)
                    
                    logger.info('Hit on article:%s and assigned to %s' % (self.sanitize(elem['title']), regex[0]))
                
                    self.browser.post(editTagURL, pParms)
                
    #----------------------------------------------------------------------
    def sanitize(self, inString):
        """Sanitize UTF-8 code by turning it into ASCII"""
        return inString.encode('ascii', 'ignore')
        
        