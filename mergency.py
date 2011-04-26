#!/usr/bin/env python
import csv, re

"""
mergency.py

This script reads CSV data and populates a text template with its 
values.  The first line of the CSV must contain field names which 
correspond to the template variable fields. Variable fields in 
the text file must be flanked by percent signs (%). The first
value of each CSV record must contain the output filename for
that record.

For example, here are the first 2 lines of a CSV data file, data.csv:

NAME,NOUN_1,VERB_1,NOUN_2
"file_one","fox","lept","emu"

Here is an example template file, template.txt:

The quick, red %NOUN_1% %VERB_1% over the lazy brown %NOUN_2%

Here's the command to run:

$ mergency.py data.csv template.tpl

The output is a file named file_one.txt, and its contents are:

The quick, red fox lept over the lazy brown emu.

"""

DATA_FILE = 'data.csv'
TEMPLATE_FILE = 'template.tpl'
OUTFILE_SUFFIX = 'txt'

template= ''
fieldKeys = ()
rowIndex = 0

# Load the template into memory
with open(TEMPLATE_FILE) as f:
  template = f.read()

# Iterate over each record in the data file to build our merged output
dataFile = csv.reader(open(DATA_FILE, 'r'), delimiter=',', quotechar='"')

for row in dataFile:
  if len(fieldKeys) == 0:
    fieldKeys = row
    continue
  # Combine the keys and row values into a map for template replacements
  valueMap = dict(zip(fieldKeys, row))

  # Create a new merged file for each subsequent row
  outFile = open(valueMap['NAME'] + '.' + OUTFILE_SUFFIX, 'w')

  # Replace key palceholders with the values from this row
  this_template = template
  for key, value in valueMap.items():
    this_template = re.sub('%' + key + '%', value, this_template, re.MULTILINE)

  # Write the output
  outFile.write(this_template)
  outFile.close()

  # Increment the counter for summary
  rowIndex += 1

print("Finished processing " + str(rowIndex) + " records.")
