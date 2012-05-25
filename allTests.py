#!/usr/bin/python

import unittest
import coverage
import logging

gotCoverage = False
printToScreen = True
unittestResultsFileName = 'unittest.results'

import os
import sys
import socket
import datetime
import shutil

#----------------------------------------------------------------------
def initializeLogging(name='FeedFiddler.log'):
	'''Routine that sets up the logging that will be utilized by the program '''
	#Set the root level prefix in the logger 
	logPrefix = 'ff'
	
	#Set the name of the log file
	logName = name
	
	#Set the filter level for this logging instance
	logLevel = logging.DEBUG
	
	#Set the message format the root level 
	messageFormat = '%(asctime)s %(name)-21s %(levelname)-6s %(message)s'
	dateFormat= '%m-%d-%y %H:%M:%S'
	
	#Setup our logging objects by definining them 
	log = logging.getLogger(logPrefix)
	log.setLevel(logLevel)
	
	logHandle = logging.FileHandler(logName)
	logFormat = logging.Formatter(messageFormat, dateFormat)
	logHandle.setFormatter(logFormat)
	log.addHandler(logHandle)
	
	return log 


#start your coverage if desired:
if gotCoverage:
	covDirectory = 'covhtml'
	cov = coverage.coverage()
	cov.start()

#import all the unit tests here so coverage will be able to register them
import testBrowser
import testGReader


#start our logging
logger = initializeLogging('unittest.log')

#ADD ALL YOUR TEST SUITES HERE
#-------------------------------------------
suiteList = []

#HTTP Browser
suiteList.append(testBrowser.getSuite())

#Google Reader
suiteList.append(testGReader.getSuite())
#-------------------------------------------


#Add all the suites to create one test
allTestSuite = unittest.TestSuite(suiteList)


if __name__=='__main__':
	#record the start time
	startTime = datetime.datetime.now()
	
	logger.info('Start test')
	reportModules = [	'browserHTTP.py',
	                         		'GReader.py' ]
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
	#record the end of the test(s)	
	endTime = datetime.datetime.now()	
	
	logger.info('Finished tests. Executed in %d seconds', (endTime-startTime).seconds)
	if testResult.wasSuccessful():
		logger.info( 'UnitTest successfully ran %d tests: output in %s' % (testResult.testsRun, unittestResultsFileName))
		print 'UnitTest successfully ran %d tests: output in %s' % (testResult.testsRun, unittestResultsFileName)
	else:
		logger.info( 'UnitTest unsuccessfully ran %d tests; errors=%d; failures=%d: output in %s' % (testResult.testsRun, \
		                                                                                          len(testResult.errors),\
		                                                                                          len(testResult.failures),\
		                                                                                          unittestResultsFileName \
		                                                                                          ))
		print 'UnitTest unsuccessfully ran %d tests; errors=%d; failures=%d: output in %s' % (testResult.testsRun, \
		                                                                                          len(testResult.errors),\
		                                                                                          len(testResult.failures),\
		                                                                                          unittestResultsFileName \
		                                                                                          )
		
