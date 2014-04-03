import csv



with open('data.csv','rU') as csvfile:
  read = csv.DictReader(csvfile, delimiter = ',')
  data = []

for i in range(100000):

  name = fake.first_name() + " " + forgery.name.last_name()
  while name in names:
    name = fake.first_name() + " " + forgery.name.last_name()
  names.append(name)

with open('output.csv', 'wb') as csvfile:
  outfile = csv.writer(csvfile, delimiter=',')
  code = 10000
  for name in names:
    outfile.writerow([name, "Dr. " + name, name + ', MD', code])
    code += 1