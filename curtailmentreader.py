# curtailmentreader.py
# Author: Daniel Ahrens
# Date: 5/12/2016
# Description Webscraper used to scrape CalISO's curtailment reports

import numpy
import csv
import tabula
import pandas as pd
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

#initiate array that will be used to compile all data into one p
cumoutput = pd.DataFrame(columns = [u'DATE', 'HOUR', 'CURT TYPE', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW'])

# iterate over available days for CalISO data
for day in list(rrule(DAILY, dtstart=parse("20160630T090000"), until=parse("20170412T170030"))):
    #get date for this iteration
    dateID = day.strftime('%b%d_%Y')
    try:
        url = 'http://www.caiso.com/Documents/Wind_SolarReal-TimeDispatchCurtailmentReport' + dateID + '.pdf'
        readinput = tabula.read_pdf(url, pages='all')

        #sometimes will read differently
        if len(readinput.columns.tolist()) == 8:
            readinput.columns = [u'DATE', u'HOUR CURT TYPE', 'Unnamed: 2', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', 'Unnamed: 7', u'CURTAILED MW']
            del readinput['Unnamed: 7']

        #the hour curtailment data 
        splithourtype = readinput[ u'HOUR CURT TYPE'].astype('str').str.split(' ', 1, expand=True)
        formattedoutput = pd.concat([readinput, splithourtype], axis=1, join='inner')
        formattedoutput.columns = [u'DATE', u'HOUR CURT TYPE', 'Unnamed: 2', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW', 'HOUR', 'CURT TYPE']

        #delete the now unnecessary column
        del formattedoutput[u'HOUR CURT TYPE']


        #with multiple pages, the output needs to be shifted together
        page1 = formattedoutput[formattedoutput['Unnamed: 2'].isnull()]
        del page1['Unnamed: 2']
        page2 = formattedoutput[formattedoutput['Unnamed: 2'].notnull()]
        del page2['CURTAILED MW']
        page2.columns = [u'DATE', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW', 'HOUR', 'CURT TYPE']
        formattedoutput = pd.concat([page1, page2])

        #rearrange columns to same order as input
        formattedoutput = formattedoutput[[u'DATE', 'HOUR', 'CURT TYPE', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW']]


        #print "Columns:", formattedoutput.columns.tolist()
        #print formattedoutput
        #readinput2 = readinput.str.split(' ')
        formattedoutput.to_csv('ctmtcsv/' + dateID + '_curtailment.csv')
        print 'Completed: ' + dateID
        cumoutput = pd.concat([cumoutput, formattedoutput])
    except:
        print 'Incomplete: ' + dateID
        continue

#DATA CHANGES FORMAT AFTER APRIL 12
#iterate over available days for CalISO data
for day in list(rrule(DAILY, dtstart=parse("20170413T090000"), until=parse("20170510T170030"))):
    #get date for this iteration
    dateID = day.strftime('%b%d_%Y')
    url = 'http://www.caiso.com/Documents/Wind_SolarReal-TimeDispatchCurtailmentReport' + dateID + '.pdf'
    try:
        readinput = tabula.read_pdf(url, pages='4-5')
    except:
        try:
            readinput = tabula.read_pdf(url, pages='4')
        except:
            break

    #at some points, this is a pain
    if len(readinput.columns.tolist()) == 8:
        readinput.columns = [u'DATE', u'HOU CURT TYPE', 'Unnamed: 2', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', 'Unnamed: 7', u'CURTAILED MW']
        del readinput['Unnamed: 7']

    #the hour curtailment data 
    splithourtype = readinput[ u'HOU CURT TYPE'].astype('str').str.split(' ', 1, expand=True)
    formattedoutput = pd.concat([readinput, splithourtype], axis=1, join='inner')
    formattedoutput.columns = [u'DATE', u'HOUR CURT TYPE', 'Unnamed: 2', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW', 'HOUR', 'CURT TYPE']

    #delete the now unnecessary column. If 
    del formattedoutput[u'HOUR CURT TYPE']
    

    #with multiple pages, the output needs to be shifted together
    page1 = formattedoutput[formattedoutput['Unnamed: 2'].isnull()]
    del page1['Unnamed: 2']
    page2 = formattedoutput[formattedoutput['Unnamed: 2'].notnull()]
    del page2['CURTAILED MW']
    page2.columns = [u'DATE', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW', 'HOUR', 'CURT TYPE']
    formattedoutput = pd.concat([page1, page2])

    #rearrange columns to same order as input
    formattedoutput = formattedoutput[[u'DATE', 'HOUR', 'CURT TYPE', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW']]
    formattedoutput.drop(formattedoutput.index[:1], inplace=True)

    #print "Columns:", formattedoutput.columns.tolist()
    #print formattedoutput
    #readinput2 = readinput.str.split(' ')
    formattedoutput.to_csv('ctmtcsv/' + dateID + '_curtailment.csv')
    print 'Completed: ' + dateID
    cumoutput = pd.concat([cumoutput, formattedoutput])

cumoutput.to_csv('ctmtcsv/cum/6_30_5_10.csv')