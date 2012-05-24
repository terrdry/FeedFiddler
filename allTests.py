import unittest
import coverage

gotCoverage = True
printToScreen = True
unittestResultsFileName = 'unittest.results'

import os
import sys
import logging
import socket
import datetime
import shutil

#start your coverage if desired:
if gotCoverage:
	covDirectory = 'covhtml'
	cov = coverage.coverage()
	cov.start()

#import all the unit tests here so coverage will be able to register them
#import testSeed

suiteList = []

#ADD ALL YOUR TEST SUITES HERE
#-------------------------------------------
#<name of suite>
#suiteEnigma= testSeed.getSuite()
#suiteList.append(suiteEnigma)
#-------------------------------------------


#Add all the suites to create one test
allTestSuite = unittest.TestSuite(suiteList)
#start our logging
#import seed

#seed.initializeLogging('unittest.log')

if __name__=='__main__':
	reportModules = []
	hndl = open(unittestResultsFileName, 'w+')
	runner = unittest.TextTestRunner(verbosity=2, stream=hndl)
	testResult = runner.run(allTestSuite)
	if printToScreen:
		hndl.seek(0)
		print ''.join(hndl.readlines())
	hndl.close()
	if gotCoverage:
		cov.stop()
		cov.save()
		cov.html_report(morfs=reportModules, directory=covDirectory)
		print 'Coverage report in %s directory' % covDirectory
		
	if testResult.wasSuccessful():
		print 'UnitTest successfully ran %d tests: output in %s' % (testResult.testsRun, unittestResultsFileName)
	else:
		print 'UnitTest unsuccessfully ran %d tests; errors=%d; failures=%d: output in %s' % (testResult.testsRun, \
		                                                                                          len(testResult.errors),\
		                                                                                          len(testResult.failures),\
		                                                                                          unittestResultsFileName \
		                                                                                          )
		
