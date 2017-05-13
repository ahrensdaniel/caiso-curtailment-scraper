import csv

def csvtodailydata(filename):
	with open(filename, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		tablecheck = 0
		for row in spamreader:
			if row.equals('Data used to produce hourly charts'):
				tablecheck = 1
			if tablecheck = 1:
				





def main():


