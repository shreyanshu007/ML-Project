import numpy as np

TOTALQUESTIONS = 97078
numOfQuestionsToBeSelected = 5000
NUM_OF_TAGS = 20

selectedQuestionsTrain = []
selectedQuestionsTest = []

print("Selecting random questions...")
while len(selectedQuestionsTrain)!=numOfQuestionsToBeSelected:
	r = np.random.randint(1, TOTALQUESTIONS+1)
	if r not in selectedQuestionsTrain:
		selectedQuestionsTrain.append(r)

while len(selectedQuestionsTest)!=numOfQuestionsToBeSelected:
	r = np.random.randint(1, TOTALQUESTIONS+1)
	if r not in selectedQuestionsTest and r not in selectedQuestionsTrain:
		selectedQuestionsTest.append(r)

print("Selected random questions.")

print("Reading questions...")
testLines = []
trainLines = []
filepath = 'preprocessedTrainQuetions.txt'  
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		if cnt in selectedQuestionsTest:
			testLines.append(line.strip())
		if cnt in selectedQuestionsTrain:
			trainLines.append(line.strip())
		line = fp.readline()
		cnt += 1

print("Read questions.")
tag_to_ind = {}
tags = []


print("Reading tags...")
filepath = 'preprocessedTrainTags.txt'
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while len(tag_to_ind)!=NUM_OF_TAGS:
		line = line.strip()
		line = line.split(" ")
		for tag in line:
			if len(tag_to_ind)==NUM_OF_TAGS:
				break
			if tag not in tags:
				tag_to_ind[tag]=len(tags)
				tags.append(tag)
		line = fp.readline()
		cnt += 1
print("Read Tags.")
# print("These are the tags:")
# print(tag_to_ind)
print("Writing Tags in a file...")
s = "sampledTags.txt"
f = open(s, "w")
for tag in tags:
	# print(it1)
	f.write(tag+",")
print("Written Tags in a file.")


print("Storing Tags...")
trainTags = []
testTags = []

with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		if cnt in selectedQuestionsTrain:
			t = [0]*NUM_OF_TAGS
			line = line.strip()
			line = line.split(" ")
			for tag in line:
				t[tag_to_ind[tag]]=1
			trainTags.append(t)
		if cnt in selectedQuestionsTest:
			t = [0]*NUM_OF_TAGS
			line = line.strip()
			line = line.split(" ")
			for tag in line:
				t[tag_to_ind[tag]]=1
			testTags.append(t)
		line = fp.readline()
		cnt += 1

print("Stored Tags.")
# print(trainTags)

print("Writing Train Questions...")
s = "sampledTrainQuestions.txt"
f = open(s, "w")
for it1 in range(0, len(trainLines)):
	# print(it1)
	f.write(trainLines[it1]+"\n")
print("Written Train Questions.")

print("Writing Test Questions...")
s = "sampledTestQuestions.txt"
f = open(s, "w")
for it1 in range(0, len(testLines)):
	f.write(testLines[it1]+"\n")
print("Written Test Questions.")


print("Writing Tags for both train and test...")
for it1 in range(0, NUM_OF_TAGS):
	# print(it1)
	s = "sampledTrainTags"+tags[it1]+".txt"
	f = open(s, "w")
	for it2 in range(0, len(trainLines)):
		if trainTags[it2][it1]==1:
			f.write("1\n")
		else:
			f.write("0\n")
	s = "sampledTestTags"+tags[it1]+".txt"
	f = open(s, "w")
	for it2 in range(0, len(testLines)):
		if testTags[it2][it1]==1:
			f.write("1\n")
		else:
			f.write("0\n")
print("Written Tags for both train and test.")

print("Finished.")
