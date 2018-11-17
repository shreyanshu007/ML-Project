import csv 
import nltk

f = open('train.csv', encoding="utf8")

reader = csv.reader(f, delimiter=',')

i= 0
tag_list = []
word_list = []
for line in reader:
	# print(line[1])
	# if i > 1000:
	# 	break
	print(i)
	# print (line[0])
	for wro in nltk.pos_tag(line[0].split()):
		# print(nltk.pos_tag(line[0].split()))
		# print("chek")
		if(wro[1] == 'NNP'):
			word_list.append(wro[0])
	i += 1
	l = line[1]
	l = l[2:len(l)-2]
	# print("list l:", l)
	tokens = l.split('\', \'')

	for tag in tokens:
		# print("tag:", tag)
		tag_list.append(tag)

l = list(set(tag_list))
m = list(set(word_list))

print(i)
print(len(l))
print(l)


# print(m)
print(len(m))
print((m))
# print(m.index("the"))
# print(m.index("a"))
# print(m.index("is"))
