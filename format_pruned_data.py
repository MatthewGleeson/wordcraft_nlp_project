import os
import sys
import argparse
import logging

from utils import seed as utils_seed
from wordcraft.recipe_book import RecipeBook, Recipe
from utils.word2feature import FeatureMap
import json
import string
import random
import numpy as np
import collections

def main():
	wordcraft_rel_word_to_id = {'COMBINES_WITH' : 0, 'COMPONENT_OF' : 1}
	wordcraft_rel_id_to_word = {0 : 'COMBINES_WITH', 1 : 'COMPONENT_OF'}

	data_path='datasets/alchemy2pruned.json'
	f = open(data_path)
	recipe = json.load(f)
	f.close()
	max_depth = 1

	original_path = data_path='datasets/alchemy2.json'
	f = open(original_path)
	original_recipe = json.load(f)
	f.close()

	original_entities = tuple(original_recipe['entities'].keys())

	entities = tuple(recipe['entities'].keys())
	entity2index = {e : i for i, e in enumerate(original_entities) if e in entities}
	index2entity = {i : e for i, e in enumerate(original_entities) if e in entities}
	entity2recipes = collections.defaultdict(list)

	for e in entities:
	    for r in recipe['entities'][e]['recipes']:
	        if e not in r:
	            entity2recipes[e].append(Recipe(r))
	entity2recipes = dict(entity2recipes)

	combines = []
	components = []
	combines_num = []
	components_num = []

	total = 0
	for i in entity2recipes:
		for j in entity2recipes[i]:
			keys = list(j.keys())
			if len(keys) > 1:
			    combines.append(keys)
			    combines_num.append([entity2index[keys[0]], 0, entity2index[keys[1]]])
			    total += 1
			    combines.append([keys[1], keys[0]])
			    combines_num.append([entity2index[keys[1]], 0, entity2index[keys[0]]])
			    total += 1
			else:
			    combines.append([keys, keys])
			    combines_num.append([entity2index[keys[0]], 0, entity2index[keys[0]]])
			    total += 1
			for key in keys:
				if [key, i] not in components:
					components.append([key, i])
					components_num.append([entity2index[key], 1, entity2index[i]])
					total += 1

	triples = []
	for i in components_num:
		triples.append(''.join(str(j) + '\t' for j in i)[:-1] + '\n')
	for i in combines_num:
		triples.append(''.join(str(j) + '\t' for j in i)[:-1] + '\n')

	print(triples)

	relation_ids_full = []
	for key, value in wordcraft_rel_id_to_word.items():
		relation_ids_full.append(''.join(str(key) + '\t' + value + '\n'))

	id2word = []
	#for key, value in wordcraft_ent_id_to_word.items():
	for key, value in index2entity.items():
		id2word.append(''.join(str(key) + '\t' + value + '\n'))

	print(id2word)

	perm = np.random.permutation(len(triples))
	train_end = int(.8 * len(triples))
	validate_end = int(.1 * len(triples)) + train_end
	train = list(np.array(triples)[perm[:train_end]])
	validate = list(np.array(triples)[perm[train_end:validate_end]])
	test = list(np.array(triples)[perm[validate_end:]])

	train_f = open('train.del', 'w')
	val_f = open('val.del', 'w')
	test_f = open('test.del', 'w')
	#entity_ids_full_f = open('entity_ids.del', 'w')
	#entity_strings_full_f = open('entity_strings.del', 'w')
	relation_ids_full_f = open('relation_ids.del', 'w')
	id_to_word = open('entity_ids.del', 'w')

	for line in id2word:
		id_to_word.write(line)

	for line in train:
		train_f.write(line)

	for line in validate:
		val_f.write(line)

	for line in test:
		test_f.write(line)

	#for line in entity_strings_full:
		#entity_ids_full_f.write(line)

	#for line in entity_ids_full:
		#entity_strings_full_f.write(line)

	for line in relation_ids_full:
		relation_ids_full_f.write(line)

	train_f.close()
	#entity_ids_full_f.close()
	#entity_strings_full_f.close()
	relation_ids_full_f.close()
	id_to_word.close()
	val_f.close()
	test_f.close()

if __name__ == '__main__':
	main()
