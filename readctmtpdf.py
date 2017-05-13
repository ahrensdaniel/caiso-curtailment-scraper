import pdftables_api
from numpy import *


c = pdftables_api.Client('5q0tm9aktlp5');
c.csv('ctmtpdf/pdf/mar/Wind_SolarReal-TimeDispatchCurtailmentReportMar01_2017.pdf', 
	'ctmtpdf/csv/mar/Wind_SolarReal-TimeDispatchCurtailmentReportMar01_2017.csv');

