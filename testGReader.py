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
			ggAccount.authenticate()
		except GReader.googleReaderError,e:
			self.fail()
			
		
	##----------------------------------------------------------------------
	#def testGoogleReaderBadLogin(self):
		#""" Attempt to login using bad credentials account"""
		#try:
			#ggAccount  = GReader.googleReader()
		
			##monkeypatch it so that the password is wrong
			#ggAccount.password = "wrongPassword"
			#ggAccount.authenticate()
			
			##if we got this far, its bad, really bad
			#self.fail()
		#except GReader.googleReaderError:
			#pass
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
		ggAccount.authenticate()
		self.ggAccount = ggAccount
		
	#----------------------------------------------------------------------
	def testGoogleReaderSubscriptionList(self):
		""" Test that we can list out our subscriptions"""
		
		try:
			resList = self.ggAccount.listFeeds()
			
			if not resList:
				self.fail()
			
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def testGoogleReaderTagList(self):
		""" Test that we can list out our tags """
		
		try:
			resList = self.ggAccount.listTags()
			
			if not resList:
				self.fail()
				
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def testGoogleReaderArticleList(self):
		""" Test that we can list out our articles """
		
		try:
			resList = self.ggAccount.listArticles()
			
			if not resList:
				self.fail()
				
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def tearDown(self):
		pass

########################################################################
class TestGoogleReaderTagging(unittest.TestCase):
	"""Test the Google Reader Interface search/tagging capabilities"""
	#----------------------------------------------------------------------
	def setUp(self):
		"""Initialization"""
		#create our reader
		ggAccount  = GReader.googleReader()
		
		#login to google
		ggAccount.authenticate()
		self.ggAccount = ggAccount
	#----------------------------------------------------------------------
	def testSearchReplace(self):
		""" Test that we can connect to our google reader account"""
		
		try:
			self.ggAccount.listAndTagArticles()
			
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def testUserInfo(self):
		""" Test that we can see our userInfo"""
		
		try:
			userInfoText = self.ggAccount.getUserInfo()
			
		except GReader.googleReaderError,e:
			self.fail()
	#----------------------------------------------------------------------
	def tearDown(self):
		pass

def getSuite():
	suiteList = []
	suiteList.append(unittest.makeSuite(TestGoogleReaderSimple))
	suiteList.append(unittest.makeSuite(TestGoogleReaderListings))
	suiteList.append(unittest.makeSuite(TestGoogleReaderTagging))
	return unittest.TestSuite(suiteList)