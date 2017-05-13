import numpy
import csv
import tabula
import pandas as pd
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

# def squeeze_nan(x):
#     original_columns = x.index.tolist()

#     squeezed = x.dropna()
#     squeezed.index = [original_columns[n] for n in range(squeezed.count())]

#     return squeezed.reindex(original_columns, fill_value=numpy.nan)


# readinput = tabula.read_pdf("http://www.caiso.com/Documents/Wind_SolarReal-TimeDispatchCurtailmentReportApr21_2017.pdf", pages='4')
# readinput.drop(readinput.index[:1], inplace=True)

# print len(readinput.columns.tolist())
# print readinput

url = 'http://www.caiso.com/Documents/Wind_SolarReal-TimeDispatchCurtailmentReportJul17_2016.pdf'
readinput = tabula.read_pdf(url, pages='all')

print readinput
#sometimes will read differently
print len(readinput.columns.tolist())
if len(readinput.columns.tolist()) == 8:
    readinput.columns = [u'DATE', u'HOUR CURT TYPE', 'Unnamed: 2', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', 'Unnamed: 7', u'CURTAILED MW']
    del readinput['Unnamed: 7']
    print 'should drop after this'
    print readinput

#the hour curtailment data 
splithourtype = readinput[ u'HOUR CURT TYPE'].astype('str').str.split(' ', 1, expand=True)
formattedoutput = pd.concat([readinput, splithourtype], axis=1, join='inner')
print formattedoutput
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
print formattedoutput
cumoutput = pd.concat([cumoutput, formattedoutput])



#splithourtype = readinput[ u'HOUR CURT TYPE'].astype('str').str.split(' ', 1, expand=True)
#formattedoutput = pd.concat([readinput, splithourtype], axis=1, join='inner')
#formattedoutput.columns = [u'DATE', u'HOUR CURT TYPE', 'Unnamed: 2', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW', 'HOUR', 'CURT TYPE']

#delete now unnecessary columns
#del formattedoutput[u'HOUR CURT TYPE']
#del formattedoutput['Unnamed: 2']
#print formattedoutput

#page1 = formattedoutput[formattedoutput['Unnamed: 2'].isnull()]
#del page1['Unnamed: 2']
#page2 = formattedoutput[formattedoutput['Unnamed: 2'].notnull()]
#del page2['CURTAILED MW']
#page2.columns = [u'DATE', u'REASON', u'FUEL TYPE', u'CURTAILED MWH', u'CURTAILED MW', 'HOUR', 'CURT TYPE']
#formattedoutput = pd.concat([page1, page2])


#print "Columns:", formattedoutput.columns.tolist()
#print formattedoutput
#readinput2 = readinput.str.split(' ')
#readinput2.to_csv('readinput.csv')df.isnull().T.any().T

