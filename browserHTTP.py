import logging

import urllib
import urllib2
import cookielib

#########################################################################
class processingHTTPError(Exception):    
    """Processing Error Exception stub """
    

########################################################################
class  browserHTTP(object):
    """ Simple browser with cookies"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        self.txHeaders = {}
        self.txHeaders['User-agent'] = 'Mozilla/4.0 (compatible;MSIE5.5;Windows NT)'
        self.txHeaders['Content-type'] = 'application/x-www-form-urlencoded'
        
        """setup brwser, init cookie lib"""
        opener = urllib2.build_opener(urllib2.HTTPHandler())
        urllib2.install_opener(opener)
        self.urlopen = urllib2.urlopen
        self.Request = urllib2.Request
    #----------------------------------------------------------------------
    def post(self,url, postData):
        """Open this URL, return text of page"""
        try:
            req = self.Request(url, postData, self.txHeaders)
            handle = self.urlopen(req)
            return handle.read().strip()
        except urllib2.HTTPError, e:
            raise processingHTTPError(e.code)
    #----------------------------------------------------------------------
    def get(self,url):
        """Open this URL, return text of page"""
        try:
            req = self.Request(url, None, self.txHeaders)
            handle = self.urlopen(req)
            return handle.read().strip()
        except urllib2.HTTPError, e:
            raise processingHTTPError(e.code)
    #----------------------------------------------------------------------
    def put(self,url):
        """Open this URL, return text of page"""
        try:
            req = self.Request(url, self.postData, self.txHeaders)
            req.get_method = lambda: 'PUT'
            handle = self.urlopen(req)
            return handle.read().strip()
        except urllib2.HTTPError, e:
            raise processingHTTPError(e.code)


#----------------------------------------------------------------------
def urlEncode( params):
    """URL encoding without the special characters"""
    return urllib.unquote(urllib.urlencode(params))
            
        
        
    
    