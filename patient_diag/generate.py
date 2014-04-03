import csv
import json 
import re
import sys

with open('../zippop.csv','rU') as zippop:
  zpop = csv.reader(zippop, delimiter = ',')
  zpop.next()
  zips = {}
  for row in zpop:
    x = row[0]
    x = x[:-2]
    if x not in zips:
      zips[x] = row[1]
    else:
      zips[x] = int(zips[x]) + int(row[1])

  with open('../data.csv','rU') as csvinfile:
    read = csv.DictReader(csvinfile, delimiter = ',')
    read.next()
    diagnosis = []
    name = ""

    for row in read:
      if row['CCS Diagnosis Description'] not in diagnosis:
        diagnosis.append(row['CCS Diagnosis Description'])
        print row['CCS Diagnosis Description']
        print len(diagnosis)

    for i in diagnosis:
      csvinfile.seek(0)
      name = re.sub(r'[^\w]', ' ', i)+'.csv'
      data = {}

      for row in read:
        if row['Zip Code - 3 digits'] not in data:
          if row['Zip Code - 3 digits'] in zips:
            data[row['Zip Code - 3 digits']] = [0,zips[row['Zip Code - 3 digits']]]
          else:
            data[row['Zip Code - 3 digits']] = [0, '']
        if row['CCS Diagnosis Description'] == i:
          stuff = data[row['Zip Code - 3 digits']]
          count = stuff[0]
          count += 1
          data[row['Zip Code - 3 digits']] = [count,stuff[1]]

      with open(name, 'w') as csvoutfile:
        output = csv.writer(csvoutfile, delimiter=',')
        output.writerow(['id','count','population'])
        for key in data:
          if key != 'CCS Diagnosis Description':
            output.writerow([str(key)+'00', str(data[key][0]), str(data[key][1])])
        print name