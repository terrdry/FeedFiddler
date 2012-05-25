import logging

import ConfigParser



########################################################################
class  grInterface(object):
    """ Simple interface for Google Reader"""
    #----------------------------------------------------------------------
    def __init__(self):
        """ Constructor """
        #read an initialization file that contains the values for the authentication tokens
        configs = ConfigParser.ConfigParser()
        configs.read('FeedFiddler.ini')
        
        #Password authentication method
        self.username = configs.get('SECURITY', 'username')
        self.password = configs.get('SECURITY', 'password')
    def login(self):
        """Login to the service with your built in authentication method"""
        pass
    
    