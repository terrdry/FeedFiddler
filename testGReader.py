import unittest
import re

import logging
logger = logging.getLogger('ff.%s' % __name__)

import GReader

########################################################################
class TestGoogleReaderSimple (unittest.TestCase):
	""" Elementary tests for logging into the Google Reader Authentication system"""
	#----------------------------------------------------------------------
	def setUp(self):
		"""Initialization"""
		pass
	#----------------------------------------------------------------------
	def testGoogleReaderLogin(self):
		""" Test that we can connect to our google reader account"""
		try:
			#create our reader
			ggAccount  = GReader.googleReader()
			
			#login to google
			ggAccount.login()
		except GReader.googleReaderError,e:
			self.fail()
			
		
		#see if we can list our feeds
		#ggAccount.listFeeds()
		
		#result = myBrowser.post(targetURL)
		#if re.search("Feeling Lucky", result):
			#assert True
		#else:
			#self.fail()
	#----------------------------------------------------------------------
	def testGoogleReaderBadLogin(self):
		""" Attempt to login using bad credentials account"""
		try:
			ggAccount  = GReader.googleReader()
		
			#monkeypatch it so that the password is wrong
			ggAccount.password = "wrongPassword"
			ggAccount.login()
			
			#if we got this far, its bad, really bad
			self.fail()
		except GReader.googleReaderError:
			pass
	#----------------------------------------------------------------------
	def tearDown(self):
		pass
	
	
########################################################################
class TestGoogleReaderListings(unittest.TestCase):
	"""Test the Google Reader Interface Listing capabilities"""
	#----------------------------------------------------------------------
	def setUp(self):
		"""Initialization"""
		#create our reader
		ggAccount  = GReader.googleReader()
		
		#login to google
		ggAccount.login()
		self.ggAccount = ggAccount
		
	#----------------------------------------------------------------------
	def testGoogleReaderSubscriptionList(self):
		""" Test that we can connect to our google reader account"""
		
		try:
			resList = self.ggAccount.listFeeds()
			
			if not resList:
				self.fail()
			
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def testGoogleReaderTagList(self):
		""" Test that we can connect to our google reader account"""
		
		try:
			resList = self.ggAccount.listTags()
			
			if not resList:
				self.fail()
				
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def testGoogleReaderArticleList(self):
		""" Test that we can connect to our google reader account"""
		
		try:
			resList = self.ggAccount.listArticles()
			
			if not resList:
				self.fail()
				
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def tearDown(self):
		pass


def getSuite():
	suiteList = []
	suiteList.append(unittest.makeSuite(TestGoogleReaderSimple))
	suiteList.append(unittest.makeSuite(TestGoogleReaderListings))
	return unittest.TestSuite(suiteList)