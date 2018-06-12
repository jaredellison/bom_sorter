#--------------------------------------------------------------------
# BOM_Sort
# Version 0.1
# 1 - 4 - 18
#
# An electronics bill of materials contains values like 10k, 1uF and
# 1pf. The abreviated orders of magnitude make it easier to think about
# an enormous range of values but it is not easy to sort a spreadsheet 
# by part values.
# 
# This script takes a csv file exported from the Electronics CAD program
# Diptrace, finds the values field and sorts the component values from 
# least to greatest to make organizing parts and assembling circuit boards
# based on the BOM easier.
# 
# To do:
#    - Accept file name as command line argument
#    - Use original file name as basis for output file name
#--------------------------------------------------------------------

debug = False

#-----------------------------------------------
# Function: valueParser
# arg1: component is either "RES" or "CAP"
# arg2: digit plus "r","R","k","K","m","M","pF","pf","p","nF","nf","n","uF","uf","u"
#
# returns: a list including "RES" or "CAP" and a numeric value as a string
#
# This function converts an engineering shorthand like "10k" to a number like 10,000
#-----------------------------------------------

def valueParser(component, value):
	if component == 'RES':
		if 'R' in value or 'r' in value:
			value = value.replace('R','')
			value = value.replace('r','')
			value = float(value)
			# string formatting ensures output
			# is not printed in scientific notation
			# and includes leading zeros for easy string sorting
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'RES', value
		if 'K' in value or 'k' in value:
			value = value.replace('K','')
			value = value.replace('k','')
			value = float(value)
			value = round(value * 1000, 2)
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'RES', value
		if 'M' in value or 'm' in value:
			value = value.replace('M','')
			value = value.replace('m','')
			value = float(value)
			value = round(value * 1000000, 2)
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'RES', value
	if component == 'CAP':
		#---------------------------
		# Picofarads
		#---------------------------
		if 'pF' in value:
			loc = value.find('pF')
			value = value[:loc]
			value = value * 1e-12
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		elif 'pf' in value:
			loc = value.find('pf')
			value = value[:loc]
			value = float(value)
			value = value * 1e-12
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		elif 'p' in value:
			loc = value.find('p')
			value = value[:loc]
			value = float(value)
			value = value * 1e-12
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		#---------------------------
		# Nanofarads
		#---------------------------
		elif 'nF' in value:
			loc = value.find('nF')
			value = value[:loc]
			value = float(value)
			value = value * 1e-9
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		elif 'nf' in value:
			loc = value.find('nf')
			value = value[:loc]
			value = float(value)
			value = value * 1e-9
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		elif 'n' in value:
			loc = value.find('n')
			value = value[:loc]
			value = float(value)
			value = value * 1e-9
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		#---------------------------
		# Microfarads
		#---------------------------
		elif 'uF' in value:
			loc = value.find('uF')
			value = value[:loc]
			value = float(value)
			value = value * 1e-6
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		elif 'uf' in value:
			loc = value.find('uf')
			value = value[:loc]
			value = float(value)
			value = value * 1e-6
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value
		elif 'u' in value:
			loc = value.find('u')
			value = value[:loc]
			value = float(value)
			value = value * 1e-6
			value = "{0:.12f}".format(value)
			value = "{0:0>24}".format(value)
			return 'CAP', value

#----------------------------------------
#
# Open source csv file
#
#----------------------------------------

dataFile = open('Example BOM To Be Sorted.csv','rb')

totalLines = []

# Line Counter
i = 0

for line in dataFile:
	# Unicode encoding prevents "'b" from printing before string
	line = str(line,'utf-8')

	# Extract the first line of the file as heading.
	if i == 0:
		header = line.split(',')
		# Create a temporary copy of this list
		headercopy = []
		for item in header:
			# Remove all quotes and newline characters
			item = item.replace('"','')
			item = item.replace('\r\n','')
			headercopy.append(item)
		header = headercopy[:]

		if debug:
			print('-' * 50)
			print(headercopy)
			print('-' * 50)


	# For the rest of the lines, add them to the list of
	# total lines. This is our dataset.
	else:
		linecopy = []
		line = line.split('","')
		for item in line:
			item = item.replace('"','')
			item = item.replace('\r\n','')
			linecopy.append(item)
		line = linecopy[:]
		totalLines.append(line)
	i += 1

if debug:
	print(totalLines)
	print('-' * 60 + '\n' * 4)


# Add header columns to sort components by
header.append("componentSorter")
header.append("valueSorter")

# Find the indexes for the columns that contain
# component values and names
nameColumn = header.index('Name')
valueColumn = header.index('Value')

# Check each line to see if a compnent is a capacitor or resistor
# and if so, pass the value to the valueParser function and append
# the full numeric value of the part to the line.

totalLineCopy = []
for line in totalLines:
	if 'CAP' in line[nameColumn]:
		if debug:
			print('Cap ---> ' + line[valueColumn])
			print('Parsed Value ---> ' + str(valueParser('CAP',line[valueColumn])))
		parsedValue = valueParser('CAP',line[valueColumn])
		line.append(parsedValue[0])
		line.append(parsedValue[1])

	elif 'RES' in line[nameColumn]:
		if debug:
			print('Res ---> ' + line[valueColumn])
			print('Parsed Value ---> ' + str(valueParser('RES',line[valueColumn])))
		parsedValue = valueParser('RES',line[valueColumn])
		line.append(parsedValue[0])
		line.append(parsedValue[1])
	
	else:
		line.append('')
		line.append('')
	totalLineCopy.append(line)

totalLines = totalLineCopy[:]

if debug:
	print('\n' * 4)
	print('-' * 60)
	print(header)
	print('-' * 60)
	print()
	for line in totalLines:
		print(line)


#-------------------
# Sort all lines based first on the component type then on the component value
#-------------------

componentSorterColumn = header.index('componentSorter')
valueSorterColumn = header.index('valueSorter')

totalLines = sorted(totalLines, key=lambda x : (x[componentSorterColumn],x[valueSorterColumn]))


if debug:
	print('\n' * 4)
	print('-' * 60)
	print('Sorted Lists:')
	print(header)
	print('-' * 60)
	print()
	for line in totalLines:
		print(line)


#----------------------------------------
#
# Create a file and store script output.
#
#----------------------------------------

outputFile = open("Sorted Output.csv", 'w')

tempLine = ''
for item in header:
	tempLine += '"' + item + '"\t'
tempLine = tempLine[:-1] + '\n'
outputFile.write(tempLine)		


for line in totalLines:
	tempLine = ''
	for item in line:
		tempLine += '"' + item + '"\t'
	tempLine = tempLine[:-1] + '\n'
	outputFile.write(tempLine)

outputFile.close()
