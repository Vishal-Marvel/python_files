import csv
csv.register_dialect('my', quotechar='"', quoting=csv.QUOTE_ALL)
f = open("sample.csv", 'r')
r = csv.DictReader(f, dialect='my')
d = dict(r)
print(d)
f.close()