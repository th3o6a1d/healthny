import csv
import json 


def zips(infile, outfile, hospital):
  with open(infile,'rU') as csvfile:
    read = csv.DictReader(csvfile, delimiter = ',')
    excluded = 0

    data = {}
    read.next()

    for row in read:
      if row['Zip Code - 3 digits'] not in data:
        data[row['Zip Code - 3 digits']] = 0
      if row['Facility Name'] == hospital:
        count = data[row['Zip Code - 3 digits']]
        count += 1
        data[row['Zip Code - 3 digits']] = count
    print data

  with open(outfile, 'wb') as csvfile:
    output = csv.writer(csvfile, delimiter=',')
    output.writerow(['id','rate'])
    for key in data:
      output.writerow([str(key)+'00', str(data[key])])
      print "saving data: " + key

if __name__ == "__main__":
    import sys
    zips(sys.argv[1],sys.argv[2],sys.argv[3])