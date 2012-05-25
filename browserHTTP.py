import logging

import urllib
import urllib2
import cookielib



########################################################################
class  browserHTTP(dict):
    """ Simple browser with cookies"""
    urlopen = None
    Request = None
    cookieJar = None
    
    #Stock headers
    postData = None

    #----------------------------------------------------------------------
    def __init__(self):
        self.txHeaders = {}
        self.txHeaders['User-agent'] = 'Mozilla/4.0 (compatible;MSIE5.5;Windows NT)'
        self.txHeaders['Content-Type'] = 'application/json; charset=UTF-8'
        """setup brwser, init cookie lib"""
        self.cookieJar = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        urllib2.install_opener(opener)
        self.urlopen = urllib2.urlopen
        self.Request = urllib2.Request
    def post(self,url):
        """Open this URL, return text of page"""
        req = self.Request(url, self.postData, self.txHeaders)
        handle = self.urlopen(req)
        return handle.read().strip()
    def put(self,url):
        """Open this URL, return text of page"""
        req = self.Request(url, self.postData, self.txHeaders)
        req.get_method = lambda: 'PUT'
        handle = self.urlopen(req)
        return handle.read().strip()
        
    
    