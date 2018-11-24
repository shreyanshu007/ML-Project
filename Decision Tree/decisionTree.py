filepath = 'sampledTrainQuestions.txt'
trainQuestions = []
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		trainQuestions.append(line.strip())
		line = fp.readline()
		cnt += 1

filepath = 'sampledTestQuestions.txt'
testQuestions = []
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		testQuestions.append(line.strip())
		line = fp.readline()
		cnt += 1

# print(trainQuestions)
# get nouns, make list of all nouns, fill with data, read results from file, use sklearn
import nltk

nouns = [] #empty to array to hold all nouns
cnt=1
for question in trainQuestions:
	# print(cnt)
	words = nltk.word_tokenize(question)
	for word,pos in nltk.pos_tag(words):
		if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
			nouns.append(word)
	cnt +=1
nouns = list(set(nouns))
print(nouns)
print(len(nouns))

num_of_nouns = len(nouns)
X_train = []
X_test = []
for question in trainQuestions:
	data = [0]*num_of_nouns
	for it1 in range(0, num_of_nouns):
		if nouns[it1] in question:
			data[it1] = 1
	X_train.append(data)


for question in testQuestions:
	data = [0]*num_of_nouns
	for it1 in range(0, num_of_nouns):
		if nouns[it1] in question:
			data[it1] = 1
	X_test.append(data)

filepath = 'sampledTrainTagsc++.txt'
Y_train = []
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		line = line.strip()
		Y_train.append(int(line))
		line = fp.readline()
		cnt += 1

filepath = 'sampledTestTagsc++.txt'
Y_test = []
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	while line:
		line = line.strip()
		Y_test.append(int(line))
		line = fp.readline()
		cnt += 1


print(len(Y_train), len(X_train))
print("Learning...")
from sklearn.tree import DecisionTreeClassifier  
classifier = DecisionTreeClassifier()  
classifier.fit(X_train, Y_train)
print("Learnt.")

print("Predicting...")
c=0
c2=0
res = classifier.predict(X_train)
res2 = classifier.predict(X_test)

for it1 in range(0, len(X_train)):
	if res[it1]!=Y_train[it1]:
		c +=1
y=0
for it1 in range(0, len(X_test)):
	if res2[it1]!=Y_test[it1]:
		c2 +=1
	if res2[it1]==1:
		y +=1

print(c,c2,y)