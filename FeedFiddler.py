#!/usr/bin/python
import logging
import datetime

import GReader

#----------------------------------------------------------------------
def initializeLogging(name='FeedFiddler.log', loggingLevel= logging.DEBUG ):
	'''Routine that sets up the logging that will be utilized by the program '''
	#Set the root level prefix in the logger 
	logPrefix = 'ff'
	
	#Set the name of the log file
	logName = name
	
	#Set the filter level for this logging instance
	logLevel = loggingLevel
	
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


if __name__=='__main__':
	#start our logging
	logger = initializeLogging(loggingLevel=logging.INFO)
	
	#record the start time
	startTime = datetime.datetime.now()
	
	#create our reader interface object
	ggAccount = GReader.googleReader()
	
	#login to google
	ggAccount.authenticate()
	
	ggAccount.listAndTagArticles()
	
	#record the end of the run
	endTIme = datetime.datetime.now()
	logger.info('Completed run in %d seconds' % (endTIme-startTime).seconds)
    
    
    
