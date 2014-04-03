import csv
from faker import Factory
from forgery_py import forgery

# pip install Forgery.py to get the forgery module
# pip install fake-factory to get the faker module
# import the Factory and set the locale to english/US
# note: the forgery module doesn't produce consistently gender-balanced first names, but the last names are less ridiculous than faker

fake = Factory.create('en_US')
names = []

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