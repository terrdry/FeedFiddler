import unittest
import re

import logging
logger = logging.getLogger('ff.%s' % __name__)

import GReader

########################################################################
class TestGoogleReaderSimple (unittest.TestCase):
	"""Test the Google Reader Interface"""
	#----------------------------------------------------------------------
	def setUp(self):
		"""Initialization"""
		pass
	#----------------------------------------------------------------------
	def testGoogleReaderLogin(self):
		""" Test that we can connect to our google reader account"""
		logger.debug('attempting to  activate google reader account')
		ggAccount  = GReader.grInterface()
		
		
		myID = ggAccount.login()
		
		#see if we can list our feeds
		ggAccount.listFeeds()
		
		#result = myBrowser.post(targetURL)
		#if re.search("Feeling Lucky", result):
			#assert True
		#else:
			#self.fail()
	#----------------------------------------------------------------------
	def tearDown(self):
		pass


def getSuite():
	suiteList = []
	suiteList.append(unittest.makeSuite(TestGoogleReaderSimple, 'test'))
	return unittest.TestSuite(suiteList)