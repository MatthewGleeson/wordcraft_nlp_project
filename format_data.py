import os
import sys
import argparse
import logging

from utils import seed as utils_seed
from wordcraft.recipe_book import RecipeBook
from utils.word2feature import FeatureMap
import json
import string
import random
import numpy as np

def main():

	f = open('datasets/alchemy2.json')
	recipe = json.load(f)
	recipe_ids = [recipe['entities'][i]['id'] for i in recipe['entities']]
	f.close()

	wordcraft_rel_word_to_id = {'COMBINES_WITH' : 0, 'COMPONENT_OF' : 1}
	wordcraft_rel_id_to_word = {0 : 'COMBINES_WITH', 1 : 'COMPONENT_OF'}

	wordcraft_ent_word_to_id = {}
	wordcraft_ent_id_to_word = {}

	for i in recipe['entities']:
	    wordcraft_ent_word_to_id[i] = recipe['entities'][i]['id']
	    wordcraft_ent_id_to_word[recipe['entities'][i]['id']] = i

	chars = string.ascii_lowercase + string.digits

	wordcraft_ent_word_to_code = {}
	wordcraft_ent_code_to_word = {}
	wordcraft_ent_id_to_code = {}
	wordcraft_ent_code_to_id = {}

	strings = set()

	for i in recipe_ids:
	    s = "/m/"
	    prop = s + ''.join(random.choice(chars) for i in range(5))
	    while prop in strings:
	        prop = prop + random.choice(chars)
	    strings.add(prop)
	    wordcraft_ent_word_to_code[wordcraft_ent_id_to_word[i]] = prop
	    wordcraft_ent_code_to_word[prop] = wordcraft_ent_id_to_word[i]
	    wordcraft_ent_id_to_code[i] = prop
	    wordcraft_ent_code_to_id[prop] = i

	combines = []
	components = []
	combines_num = []
	components_num = []

	for i in recipe['entities']:
	    for j in recipe['entities'][i]['recipes']:
	        combines.append(j)
			combines.append([j[1], j[0]])
	        combines_num.append([recipe['entities'][combines[-1][0]]['id'], 0, recipe['entities'][combines[-1][1]]['id']])
			combines_num.append([recipe['entities'][combines[-1][1]]['id'], 0, recipe['entities'][combines[-1][0]]['id']])
	        if [j[0], i] not in components:
	            components.append([j[0], i])
	            components_num.append([recipe['entities'][components[-1][0]]['id'], 1, recipe['entities'][components[-1][1]]['id']])
	        if [j[1], i] not in components:
	            components.append([j[1], i])
	            components_num.append([recipe['entities'][components[-1][0]]['id'], 0, recipe['entities'][components[-1][1]]['id']])

	triples = []
	for i in components_num:
	    triples.append(''.join(str(j) + '\t' for j in i)[:-1] + '\n')
	for i in combines_num:
	    triples.append(''.join(str(j) + '\t' for j in i)[:-1] + '\n')

	entity_ids_full = []
	for key, value in wordcraft_ent_id_to_code.items():
	    entity_ids_full.append(''.join(str(key) + '\t' + value + '\n'))

	entity_strings_full = []
	for key, value in wordcraft_ent_code_to_word.items():
	    entity_strings_full.append(''.join(str(key) + '\t' + value + '\n'))

	relation_ids_full = []
	for key, value in wordcraft_rel_id_to_word.items():
	    relation_ids_full.append(''.join(str(key) + '\t' + value + '\n'))

	id2word = []
	for key, value in wordcraft_ent_id_to_word.items():
		id2word.append(''.join(str(key) + '\t' + value + '\n'))

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
