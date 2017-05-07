import itertools
import csv

def itergrid(x, y):
	return itertools.product(xrange(x), xrange(y))

def parse_level(path):
	level = {}
	with open(path, "rb") as file:
		reader = csv.reader(file)

		for y, row in enumerate(reader):
			for x, val in enumerate(row):
				level[x, y] = int(val)

	return level