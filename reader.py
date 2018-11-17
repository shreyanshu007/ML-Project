import csv 

f = open('train.csv', encoding="utf8")

reader = csv.reader(f, delimiter=',')

i= 0
tag_list = []
for line in reader:
	# print(line[1])
	# if i > 1000:
	# 	break
	# print(i)
	i += 1
	l = line[1]
	l = l[2:len(l)-2]
	# print("list l:", l)
	tokens = l.split('\', \'')

	for tag in tokens:
		# print("tag:", tag)
		tag_list.append(tag)

l = list(set(tag_list))

print(i)
print(len(l))
print(l)