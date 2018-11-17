import csv 
import nltk
import numpy as np
from collections import Counter

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

def reader(filename):

	f = open(filename, encoding="utf8")

	reader = csv.reader(f, delimiter=',')
	no_of_examples = 0

	tag_list = []
	word_list = []
	for line in reader:

		no_of_examples += 1
		for word in nltk.pos_tag(line[0].split()):
			if word[1] in NOUNS:
				word_list.append(word[0])

		l = line[1]
		l = l[2:len(l)-2]
		tokens = l.split('\', \'')

		for tag in tokens:
			tag_list.append(tag)

	l = list(set(tag_list))
	m = list(set(word_list))

	return l, m, no_of_examples


def feature_matrix(filename, tags, nouns, no_of_examples):

	f = open(filename, encoding="utf8")

	reader = csv.reader(f, delimiter=',')

	data = np.zeros(shape=(no_of_examples, len(nouns)), dtype=int)
	tag_vs_words = np.zeros(shape=(len(tags), len(nouns)), dtype=int)
	i = 0
	total_noun_dict = {}

	for line in reader:

		noun_list = []
		for word in nltk.pos_tag(line[0].split()):
			if word[1] in NOUNS:
				noun_list.append(word[0])

		noun_dict = Counter(noun_list)
		noun_dict_keys = noun_dict.keys()

		for key in noun_dict_keys:

			index = nouns.index(key)
			data[i][index] = noun_dict[key]

			if key in total_noun_dict.keys():
				total_noun_dict[key] += noun_dict[key]
			else:
				total_noun_dict.update({key: noun_dict[key]})
		# values = nl.values()
		# for value in values:
		# 	if value > 2:
		# 		print(nl)
		# 		break
		i += 1
		if i >= no_of_examples:
			break

		l = line[1]
		l = l[2:len(l)-2]
		tokens = l.split('\', \'')

		for token in tokens:

			for noun in noun_dict_keys:

				index1 = tags.index(token)
				index2 = nouns.index(noun)
				tag_vs_words[index1][index2] += noun_dict[noun]


	print(tag_vs_words)
	print("sum of tags values: ", np.sum(tag_vs_words))
	print("data: ", data[50][50])
	print("sum of values: ", sum(data[np.where(data > 0)]))
	# print("total_noun_dict: ", total_noun_dict)

	return data, tag_vs_words


tags, nouns, no_of_examples = reader('train.csv')
print("data read and tags extracted")
print("tag index:", tags.index('maven'))
data, tag_vs_words = feature_matrix('train.csv', tags, nouns, 10000)
