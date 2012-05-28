import unittest
import re

import logging
logger = logging.getLogger('ff.%s' % __name__)

import browserHTTP
#the following module has the error object that browserHTTP will be throwing
import urllib2

########################################################################
class TestBrowser (unittest.TestCase):
	"""Test the Browser"""
	#----------------------------------------------------------------------
	def setUp(self):
		"""Initialization"""
		pass
	#----------------------------------------------------------------------
	def testBrowserLogin(self):
		""" Test that we can connect to a web page"""
		targetURL = "http://www.google.com"
		logger.debug('attempting to  login to %s' % targetURL )
		myBrowser = browserHTTP.browserHTTP()
		
		result = myBrowser.post(targetURL, None)
		if re.search("Feeling Lucky", result):
			assert True
		else:
			self.fail()
	#----------------------------------------------------------------------
	def testBrowserBadLogin(self):
		""" Test that we can't connect to a web page"""
		targetURL = "http://www.google.com/keepout"
		logger.debug('attempting to  login to %s' % targetURL )
		myBrowser = browserHTTP.browserHTTP()
		
		try:
			result = myBrowser.post(targetURL,None)
			self.fail()
		except browserHTTP.processingHTTPError:
			assert True
	#----------------------------------------------------------------------
	def tearDown(self):
		pass


def getSuite():
	suiteList = []
	suiteList.append(unittest.makeSuite(TestBrowser, 'test'))
	return unittest.TestSuite(suiteList)