def parse(fileName):
	finalReturn = {}
	with open(fileName, "r") as file:
		data = file.read()
 
	data = data.replace("?Width=", "", 1)
	ambpos = data.find("&")
	finalReturn["Width"] = data[0:0+ambpos-1]
	data = data.replace(finalReturn["Width"], "", 1)
	data = data.replace("&Height=", "", 1)
	ambpos = data.find("&")
	finalReturn["Height"] = data[0:0+ambpos-1]
	data = data.replace(finalReturn["Height"], "", 1)
	data = data.replace("&Amount=", "", 1)
	qpos = data.find("?")
	finalReturn["Amount"] = data[0:0+qpos-1]
   
	for x in range(int(finalReturn["Width"])):
		for y in range(int(finalReturn["Height"])):
			data = data.replace("?","",1)
			keystring = "Tile" + str(x) + "#" + str(y)
			ambpos = data.find("&")
			qpos = data.find("?")
			if ambpos != -1 and ambpos < qpos: #it has properties. this is gonna be hard.
				data = data.replace("Tile=", "", 1)
				qpos = data.find("&")
				finalReturn[keystring] = data[0:0+qpos-1]
				data = data.replace(finalReturn[keystring] + "&","",1)
				ambpos = data.find("&")
				qpos = data.find("?")
				while ambpos != -1 and ambpos < qpos:
					eqpos = data.find("=")
					propertykey = data[0:0+eqpos-1]
					data = data.replace(propertykey + "=", "", 1)
					keystring = "Tile" + str(x) + "#" + str(y) + "#" + propertykey
					ambpos = data.find("&")
					finalReturn[keystring] = data[0:0+ambpos-1]
					ampbos = data.find("&")
					qpos = data.find("?")
				eqpos = data.find("=")
				propertykey = data[0:0+eqpos-1]
				data = data.replace(propertykey + "=", "", 1)
				keystring = "Tile" + str(x) + "#" + str(y) + "#" + propertykey
				qpos = data.find("?")
				finalReturn[keystring] = data[0:0+qpos-1]
			else: #it has no properties. easy peasy!
				data = data.replace("Tile=", "", 1)
				qpos = data.find("?")
				finalReturn[keystring] = data[0:0+qpos-1]
	return finalReturn

print parse("LevelOfficial.lvl")