import random
import os
import time

words = ["fly","fall","lead","cry","dark","machine","note","wait","plan","figure","star","box","noun","field","rest","correct","able","pound","done","beauty","drive","stood","contain","front","teach","week","final","gave","green","oh","quick","develop","ocean","warm","free","minute","strong","special","mind","behind","clear","tail","produce","fact","street","inch","multiply","nothing","course","stay","wheel","full","force","blue","object","decide","surface","deep","moon","island","foot","system","busy","test","record","boat","common","gold","possible","plane","stead","dry","wonder","laugh","thousand","ago"]

def generate(filename = "", continuous = False):
	loop = True
	while loop:
		folder = "/documents/"
		rndm_name = filename == ""
		if(filename == ""):
			i = 1
			while True:
				filename = "doc"+str(i)+".txt"
				if(os.path.exists(folder + filename)):
					i += 1
				else:
					break
		f = open(folder + filename, "w")
		for k in range(100):
			f.write(random.choice(words) + " ")
		f.close()
		loop = continuous
		if(loop):
			filename = ""
			time.sleep(5)


if __name__ == "__main__":
	generate()