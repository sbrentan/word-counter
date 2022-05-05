from collections import Counter

occurrences = {}
counters = {}
doc = "doc2"

def read_occurrences():
	occ_file_r = open("occurrences.txt", "r")
	lines = occ_file_r.readlines()
	occ_file_r.close()

	for line in lines:
		word, occ_txt = line.split(" ", 1)
		occurrences[word] = occ_txt.strip().split(" ")
	

def update_occurrences(counter):
	for c in counter:
		if c not in occurrences:
			occurrences[c] = [doc]
		else:
			if doc not in occurrences[c]:
				occurrences[c].append(doc)

def read_counters():
	global counters
	count_file_r = open("counters.txt", "r")
	lines = count_file_r.readlines()
	count_file_r.close()

	for line in lines:
		word, count_txt = line.split(" ", 1)
		counters[word] = int(count_txt)

	counters = Counter(counters)


filename = "documents/"+doc+".txt"

f = open(filename, "r")
data = f.read()
f.close()

words = data.split(" ")

word_counts = Counter(words)

read_counters()

read_occurrences()
update_occurrences(word_counts)

counters += word_counts

occ_file = open("occurrences.txt", "w")
for occ in occurrences.items():
	if(occ[0] != ''):
		occ_file.write(occ[0] + " " + ' '.join(occ[1]) + "\n")

occ_file.close()

count_file = open("counters.txt", "w")
for count in counters.most_common():
	if(count[0] != ''):
		count_file.write(count[0] + " " + str(count[1]) + "\n")

count_file.close()
