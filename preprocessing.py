import csv

set_of_tags = set()
with open('train.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		s = row[1][2:-2]
		r = set(s.split('\', \''))
		set_of_tags = set_of_tags|r

csvFile.close()

set_of_tags.remove("")
list_of_tags = list(set_of_tags)
# print(list_of_tags)

freq_of_tags = [0]*len(list_of_tags)

with open('train.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		s = row[1][2:-2]
		r = list(s.split('\', \''))
		for iterator in range(0, len(list_of_tags)):
			if list_of_tags[iterator] in r:
				freq_of_tags[iterator] +=1

csvFile.close()
# print(freq_of_tags)

list_of_imp_tags = list()
freq_of_imp_tags = list()
num_of_imp_tags = 20
for it1 in range(0, num_of_imp_tags):
	Max = freq_of_tags[0]
	Val = 0
	for it2 in range(0, len(list_of_tags)):
		if Max<freq_of_tags[it2]:
			Max = freq_of_tags[it2]
			Val = it2
	list_of_imp_tags.append(list_of_tags[Val])
	freq_of_imp_tags.append(freq_of_tags[Val])
	freq_of_tags[Val] = -1
	if Val==0:
		print("All tags added! Check for error!")

# print(list_of_imp_tags)
# print(freq_of_imp_tags)

Data = []

with open('train.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		s = row[1][2:-2]
		r = list(s.split('\', \''))
		data = []
		data.append(row[0])
		for iterator in range(0, len(r)):
			if r[iterator] in list_of_imp_tags:
				data.append(r[iterator])
		if len(data)>1:
			Data.append(data)

csvFile.close()

for i in range(0, len(Data)):
	Data[i] = Data[i][1:]

for it1 in range(0, len(Data)):
	for it2 in range(0, len(Data[it1])):
		print(Data[it1][it2]),
	print("")