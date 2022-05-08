import random
import os

words = ["fly","fall","lead","cry","dark","machine","note","wait","plan","figure","star","box","noun","field","rest","correct","able","pound","done","beauty","drive","stood","contain","front","teach","week","final","gave","green","oh","quick","develop","ocean","warm","free","minute","strong","special","mind","behind","clear","tail","produce","fact","street","inch","multiply","nothing","course","stay","wheel","full","force","blue","object","decide","surface","deep","moon","island","foot","system","busy","test","record","boat","common","gold","possible","plane","stead","dry","wonder","laugh","thousand","ago"]

folder = "/documents/"
i = 1
while True:
	filename = folder + "doc"+str(i)+".txt"
	if(os.path.exists(filename)):
		i += 1
	else:
		f = open(filename, "w")
		for i in range(100):
			f.write(random.choice(words) + " ")
		break

f.close()