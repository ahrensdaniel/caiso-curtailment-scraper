temp = csvread('ctmtpdf/csv/Wind_SolarReal-TimeDispatchCurtailmentReportMar01_2017.csv');
tableindexstart = find(temp == 'CURTAILED MW') + 1;
tableindexend = find(temp == 'The information contained in this report is preliminary and subject to change without notice. No inference, decision or') -1;
temp2 = temp(tableindexstart:tableindexend);