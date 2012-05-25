import unittest

import logging
logger = logging.getLogger('ff.%s' % __name__)



########################################################################
class TestXX (unittest.TestCase):
	"""Test the Pod (Pickle)"""
	#----------------------------------------------------------------------
	def setUp(self):
		"""Initialization"""
		pass
	#----------------------------------------------------------------------
	def testXXX(self):
		""" <TestDescription>"""
		pass
	#----------------------------------------------------------------------
	def tearDown(self):
		pass


def getSuite():
	suiteList = []
	suiteList.append(unittest.makeSuite(TestXX, 'test'))
	return unittest.TestSuite(suiteList)