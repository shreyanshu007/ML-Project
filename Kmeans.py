import imp
import csv 
import nltk
import numpy as np
import pickle
from collections import Counter
from sklearn.cluster import KMeans
import standarize_data as sd

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']


# function to return noun count in the given sentence.
# @param sentence: Sentence from which noun to be extracted
# @return: noun_list: list of noun words in the given sentence.
def return_nouns(sentence):

	tokens = nltk.word_tokenize(sentence)
	pos_tags = nltk.pos_tag(tokens)
	noun_list = []
	for item in pos_tags:

		if item[1] in NOUNS:
			noun_list.append(item[0])

	return noun_list


# function to extract all unique nouns in the given filename
# @param filename: name of the file
# @return total_unique_nouns: list of unique occurring nouns in the file
def extract_noun_list(filename):

	file = open(filename, 'r', encoding="utf8")

	total_unique_nouns = []
	no_of_examples = 0

	for line in file:
		no_of_examples += 1
		noun_list = return_nouns(line.strip())

		for noun in noun_list:
			if noun not in total_unique_nouns:
				total_unique_nouns.append(noun)

	return total_unique_nouns, no_of_examples


# function to extract all unique tags in the given filename
# @param filename: name of the file
# @return total_unique_nouns: list of unique occurring tags in the file
def extract_tag_list(filename):

	file = open(filename, 'r', encoding="utf8")

	total_unique_tags = []
	examples_corr_tags = {}
	no_of_examples = 0
	count = 0
	for line in file:
		no_of_examples += 1
		tag_list = line.strip().split(" ")
		examples_corr_tags[count] = line
		count += 1
		for tag in tag_list:
			if tag not in total_unique_tags:
				total_unique_tags.append(tag)

	return total_unique_tags, no_of_examples, examples_corr_tags


# function to construct a matrix of [examples X features]
def return_kmeans_matrix(filename, no_of_examples, noun_list):

	file = open(filename, 'r', encoding='utf8')
	
	kmeans_data_matrix = np.zeros(shape=(50000, len(noun_list) - 27000), dtype=float)
	count = 0
	for line in file:
		# words = nltk.word_tokenize(line)
		words = return_nouns(line)

		for word in words:
			index = noun_list.index(word)
			if index < (len(noun_list) - 27000):
				kmeans_data_matrix[count][index] += 1

		count += 1
		if count == 50000:
			return kmeans_data_matrix
	return kmeans_data_matrix


# function to condtruct a label matrix
def return_label_matrix(filename, tag_list):

	file = open(filename, 'r', encoding='utf8')

	label_matrix = np.zeros(shape=(50000, 20), dtype=float)
	count = 0
	for line in file:
		tags = line.strip().split(" ")
		for tag in tags:
			index = tag_list.index(tag)
			label_matrix[count][index] = 1

		count += 1
		if count == 50000:
			return label_matrix

	return label_matrix


def confusion_matrix_data(cluster_pred_values_final_value, clus_list, true_label):

	conf_mat = np.zeros(shape=(20,20), dtype=int)
	for i in range(50000):
		pred = cluster_pred_values_final_value[clus_list[i]]
		true = true_label[i]
		true_index = np.where(true>0)
		print(pred)
		print(true_index)
		for t in true_index[0]:
			for p in pred:
				print(t,p)
				conf_mat[t][p] += 1

	# print(conf_mat)
	for i in range(20):
		for j in range(20):
			print(conf_mat[i][j], end=" ")
		print("\n")
	return conf_mat

# main function
if __name__ == "__main__":


	print("extracting tags")
	total_tags, no_of_examples, examples_corr_tags = extract_tag_list("preprocessedTrainTags.txt")
	print("done.\n\nextracting noun list.")
	# total_nouns, _  = extract_noun_list("preprocessedTrainQuestions.txt")
	print("done.")

	# with open("total_nouns","wb") as file:
	# 	pickle.dump(total_nouns, file)

	with open("total_nouns","rb") as file:
		total_nouns = pickle.load(file)
	# np.save('total_tags', total_tags)
	# np.save('total_nouns', total_nouns)
	# total_nouns = np.load('total_nouns.npy').items()
	# print(total_tags)
	# print(len(total_nouns))
	# print(total_nouns)


	print("Proceeding for kmeans on: ", no_of_examples, " ", len(total_nouns))
	kmeans_data_matrix = return_kmeans_matrix("preprocessedTrainQuestions.txt", no_of_examples, total_nouns)
	label_matrix = return_label_matrix("preprocessedTrainTags.txt", total_tags)
	print(label_matrix)
	# kmeans_data_matrix = np.load('matrix_data.npy')
	# label_matrix = np.load('matrix_data.npy')

	kmeans_data_matrix, mean, std = sd.standarize_training_data(kmeans_data_matrix)
	print("done with kmeans standarization.")
	# mat_sum = np.sum(kmeans_data_matrix, axis=0)

	# print("saving data matrix")
	# np.save('matrix_data', kmeans_data_matrix)
	# print("matrix saved.")

	print("started kmeans clustering")
	print("shape of data sent for kmeans clustering: ", np.shape(kmeans_data_matrix[:50000,:1000]))
	k = KMeans(n_clusters=30, random_state=0).fit(kmeans_data_matrix[:50000,:200])
	print("kmeans over.")

	'''==========================================================================================='''

	# print("saving label matrix")
	# np.save('label_matrix_data', label_matrix)
	# print("matrix saved.")

	# print("clusters: ", k.cluster_centers_)
	# print("labels: ", k.labels_)

	# for i in range(10000):
	# 	for j in range(1000):
	# 		print(kmeans_data_matrix[i][j], end=" ")
	# 	print("\n")

	# for i in range(10000):
	# 	for j in range(20):
	# 		print(label_matrix[i][j], end=" ")
	# 	print("\n")
	'''====================accuracy and confusion matrix========================================='''

	cluster_pred_values = {}
	for i in range(50000):
		# exam = kmeans_data_matrix[i,:1000]
		label = label_matrix[i]
		index = np.where(label>0)
		for j in index[0]:
		# 	freq.append(exam[i])
		# # print("(cl, maxl)", k.labels_[i], max_index[0][0])
			if k.labels_[i] in cluster_pred_values.keys():
				cluster_pred_values[k.labels_[i]].append(j)
			else:
				cluster_pred_values[k.labels_[i]] = [j]


	# print(cluster_pred_values)
	cluster_pred_values_final_value = {}
	for item in cluster_pred_values.keys():
		clus_dict = Counter(cluster_pred_values[item])
		print("item: ", item, "clus: ", clus_dict)
		label_list = []
		for i in range(30):
			if i in clus_dict.keys():
				label_list.append(clus_dict[i])
			else:
				label_list.append(0)
		top_5_idx = list(np.argsort(label_list)[-3:])
		print("top 5: ", top_5_idx, "clus_dict: ", clus_dict.keys())
		for i in top_5_idx:
			if item in cluster_pred_values_final_value.keys() and i in clus_dict.keys():
				cluster_pred_values_final_value[item].append(i)
			elif i in clus_dict.keys():
				cluster_pred_values_final_value[item] = [i]


	print(cluster_pred_values_final_value)
	# confusion_matrix = np.zeros(shape=(20,20), dtype=)
	confusion_matrix_data(cluster_pred_values_final_value, k.labels_, label_matrix)

	accuracy = 0
	for example in range(50000):
		clus_label = k.labels_[example]
		if clus_label in cluster_pred_values_final_value.keys():
			pred = cluster_pred_values_final_value[clus_label]
		else:
			pred = 0
		for ind in pred:
			if label_matrix[i][ind] == 1:
				accuracy += 1
				break

	print(accuracy)
	print(accuracy/50000)




# extra things 

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