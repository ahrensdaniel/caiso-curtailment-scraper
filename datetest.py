from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

for day in list(rrule(DAILY, dtstart=parse("20160630T090000"), until=parse("20170430T000000"))):
    dateID = day.strftime('%b_%d_%Y')
    print dateID