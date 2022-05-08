from collections import Counter
import os

docs_folder = "/documents/"
documents = []
occurrences = {}
counters = {}
doc = "doc"
new_document = False

def read_occurrences():
	global occurrences
	occ_file_r = open("/save/occurrences.txt", "r")
	lines = occ_file_r.readlines()
	occ_file_r.close()

	for line in lines:
		word, occ_txt = line.split(" ", 1)
		occurrences[word] = occ_txt.strip().split(" ")


def update_occurrences(counter, doc, node_id):
	global occurrences
	for c in counter:
		if c not in occurrences:
			occurrences[c] = [node_id+"_"+doc]
		else:
			if doc not in occurrences[c]:
				occurrences[c].append(node_id+"_"+doc)

def read_counters():
	global counters
	count_file_r = open("/save/counters.txt", "r")
	lines = count_file_r.readlines()
	count_file_r.close()

	for line in lines:
		word, count_txt = line.split(" ", 1)
		counters[word] = int(count_txt)

	counters = Counter(counters)

def get_new_document():
	global documents, docs_folder
	new_docs = []
	for filename in os.listdir(docs_folder):
		if filename not in documents:
			new_docs += [filename]
	return new_docs



def update_documents(node_id):

	global doc, occurrences, counters, documents, new_document

	new_docs = get_new_document()
	if(len(new_docs) == 0):
		return;

	new_document = True
	for new_doc in new_docs:

		doc = os.path.splitext(new_doc)[0]
		filename = docs_folder+doc+".txt"
		print("Found new document: " + filename + " -> " + node_id + "_" + doc)

		f = open(filename, "r")
		data = f.read()
		f.close()

		words = data.split(" ")
		word_counts = Counter(words)

		read_counters()
		read_occurrences()
		update_occurrences(word_counts, doc, node_id)
		counters += word_counts

		occ_file = open("/save/occurrences.txt", "w")
		for occ in occurrences.items():
			if(occ[0] != ''):
				occ_file.write(occ[0] + " " + ' '.join(occ[1]) + "\n")
		occ_file.close()

		count_file = open("/save/counters.txt", "w")
		for count in counters.most_common():
			if(count[0] != ''):
				count_file.write(count[0] + " " + str(count[1]) + "\n")
		count_file.close()

		documents += [new_doc]
