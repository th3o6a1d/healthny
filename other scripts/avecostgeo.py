import csv
import json 
import httplib

with open('data.csv','rU') as csvfile:
  read = csv.DictReader(csvfile, delimiter = ',')
  excluded = 0
  cpd = 0

  data = {}
  hospital = read.next()['Facility Name']
  charges = 0
  days = 0
  average = 0
  name = ""

  for row in read:
    if row['Facility Name'] in data:
      if row['Facility Name'] == hospital:
        charges = data[row['Facility Name']][0]
        days = data[row['Facility Name']][1]
        average = data[row['Facility Name']][2]
        charges = charges + float(row['Total Charges'].strip("$").replace(',',''))
        days = days + float(row['Length of Stay'].strip("+"))
        average = charges/days
        data[row['Facility Name']][0] = charges
        data[row['Facility Name']][1] = days
        data[row['Facility Name']][2] = average
      else:
        hospital = row['Facility Name']
        total = []
    else:
      data[row['Facility Name']] = [0,0,0,"",""]
      try:
          conn = httplib.HTTPConnection("maps.googleapis.com")
          name = row['Facility Name'].replace(" ","+")
          conn.request("GET", "http://maps.googleapis.com/maps/api/geocode/json?address=" + name +"&sensor=false")
          r = conn.getresponse()
          geodata = json.load(r)
          lat = geodata['results'][0]['geometry']['location']['lat']
          lng = geodata['results'][0]['geometry']['location']['lng']
          data[row['Facility Name']][3] = lat
          data[row['Facility Name']][4] = lng
      except:
          print "reverse geocode didn't work"      
      print "working on: " + row['Facility Name']
  

with open('output.csv', 'wb') as csvfile:
  output = csv.writer(csvfile, delimiter=',')
  for key in data:
    output.writerow([key] + [data[key][2]]+ [data[key][3]] + [data[key][4]])
    print "saving data: " + key