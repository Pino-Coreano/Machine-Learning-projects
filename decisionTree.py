#!/usr/bin/python2
# -*- coding: utf-8 -*-

#__author__ = "Suo"
# ========================Part1 : User Input Training Size and Increment===========================

import operator
import matplotlib.pyplot
import sys
import numpy as np
import re
import math
import matplotlib.pyplot as plt
from numpy import *
from math import log


# Parameter to determine if input is legal
# If input legal t_S = 1
t_S = 0

# Available S
A = [250, 500, 750, 1000]

# Second version
# Determine if user's input is legal
while t_S != 1:
    try:
    	# User set size of training set
		S = input("Please enter a training set size S: (S should pick from {250, 500, 750, 1000}): \n")
		if S in A:
			t_S = 1
    except SyntaxError:
	    print "Default S = 1000"
	    S = 1000
	    t_S = 1


# Parameter to determine if input legal t_I 
# If input legal t_I = 1
t_I = 0

# Avaiable I
B = [10, 25, 50]

# Determine if user's input is legal
while t_I != 1:
    try:
    	# User set size of training set
		I = input("Please enter a training set size I: (I should pick from {10, 25, 50}): \n")
		if I in B:
			t_I = 1
    except SyntaxError:
	    print "Default I = 50"
	    I = 50
	    t_I = 1
	    

# ===========================Part 2: Load Training Set and Trainging Decision Tree==============================================

# ====Loading properties.txt=====
print "Loading Property Information from file...\n"

# Use regular expression get properties
match = re.compile(r'.*:')

# Load properties.txt
file_p = open("properties.txt", "r")
list_properties = file_p.readlines()
length_properties = len(list_properties)
for i in range(length_properties):
	list_properties[i] = match.findall(list_properties[i])
	list_properties[i][0] = list_properties[i][0].strip(":")


# keys_list list of properties name
keys_list = []
for i in range(len(list_properties)):
	k = list_properties[i][0]
	keys_list.append(k)

file_p.close()

# Copy keys list
properties_keys = []
for i in keys_list:
	properties_keys.append(i)

# properties_dict dictonary store <key, value> of properties
# value is stored as list
properties_dict = {}

# store proties and its values in dictonary
with open("properties.txt", "r") as f:
	for line in f:
		(key, value) = line.split(":")
		properties_dict[key] = value.strip("\r\n")
		properties_dict[key] = str.split(properties_dict[key])

# =============================


# ==Loading mushroom_data.txt==
print "Loading Data from database...\n"

# Load all mushroom data set
file_m = open("mushroom_data.txt", "r")
mushroom_data = file_m.readlines()
length_train = len(mushroom_data)
for i in range(length_train):
	mushroom_data[i] = mushroom_data[i].strip("\n")
	mushroom_data[i] = mushroom_data[i].split(" ")
mushroom_array = np.array(mushroom_data)
mushroom_array = mushroom_array.astype(str)
file_m.close()

print "Collecting set of", S, "examples.\n"

# Randomly select user input size data to training tree
sel = np.random.permutation(size(mushroom_array, 0))
sel = sel[0: S]

# Randomly selete from mushroom data used for training tree
all_train_array = mushroom_array[sel, :]

# rest data set used to testing decision tree
rest_data = np.delete(mushroom_array, sel, axis=0)

# ================================



# =========Decision Tree==========
def decision_tree(examples, attributes, parent_examples):
	'''
	@return: tree, list-type
	@parameter: examples, array, training set
	@parameter: list of attributes
	@parameter: parent_examples, array, parent training set
	'''

	if examples.size == 0:
		return plurality_value(parent_examples)
	elif len(classification(examples)) == 1:
		return classification(examples)[0]
	elif len(attributes) == 0:
		return plurality_value(examples)
	else:
		# a is index of attributes, as root in the tree
		a = importance(attributes, examples)

		# add tree's node
		tree = []
		tree.append(a)

		parent_examples = examples

		# split sub-tree's examples
		key = training_keys[a]
		attributes.remove(training_keys[a])
		sub_attributes = attributes
		for i in properties_dict.get(key):

			same_index = np.where(i == examples[:, a])
			for j in same_index:
				sub_examples = examples[j]
				tree.append(decision_tree(sub_examples, sub_attributes, parent_examples))
		return tree



def plurality_value(examples):
	'''
	@return: majority examples' output, "e" or "p"
	@parameter: examples, array
	'''
	count_e = 0.0000
	count_p = 0.0000
	for i in examples[:, 22]:
		if i == "e":
			count_e += 1.0000
		else:
			count_p += 1.0000

	if count_e >= count_p:
		return "e"
	else:
		return "p"


def classification(examples):
	'''
	@return: list of classification
	@parameter: examples, array
	'''
	classification_list = []
	classification_list.append(examples[0, 22])
	for i in examples[:, 22]:
		if i != classification_list[0]:
			classification_list.append(i)
			break
	return classification_list


def entropy(p):
	'''
	@return entropy h
	@parameter probability
	'''
	h = 0.0000
	if p == 0.0000 or p == 1.0000:
		return 0.0000
	else:
		part1 = p * np.log2(p)
		part2 = (1.0000 - p) * np.log2(1.0000 - p)
		h = -(part1 + part2)
		return h



def p_examples(examples):
	'''
	@return probability of examples
	@parameter examples: array
	'''
	count_e = 0.0000
	count_p = 0.0000

	for i in examples[:, 22]:
		if i == "e":
			count_e += 1.0000
		else:
			count_p += 1.0000
	return count_e/(count_p+count_e)




def importance(attributes, examples):

	'''
	@return index of impotance attribute
	@parameter attributes: list of properties
	@parameter examples: array of training dataset
	'''

	# Calculate entropy of example
	p_example = p_examples(examples)
	entropy_example = entropy(p_example)

	# Calculate gain entropy of attributes
	gain_entropy = []
	attr_entropy = []
	# get key_i in properties list
	for i in range(len(training_keys)):
		# get entropy of ley i
		key_entropy = 0.0000
		# get value_list in key_i
		for j in range(len(properties_dict.get(training_keys[i]))):
			# get value_j in key_i's value list
			value = properties_dict.get(training_keys[i])[j]
			value_entropy = 0.0000
			# scan all trainig array, get p(e) and p(p) of example j in attribute i
			'''
			count_e += len(np.where("e" == examples[:, 22] and value == examples[:, i]))
			'''
			count_e = 0.0000
			count_all = 0.0000
			for k in range(examples.shape[0]):

				if examples[k, i] == value:
					count_all += 1.0000
					if examples[k, 22] == "e":
						count_e += 1.0000

			# probability of value v_j
			if (count_e == 0 or count_all == 0):
				p_value = 0.0000
			else:
				p_value = count_e/count_all

			value_entropy += entropy(p_value)
			count_example = examples.shape[0]

			key_entropy += (count_all/count_example) * value_entropy
    
		attr_entropy.append(key_entropy)

	for i in attr_entropy:
		gain_entropy.append(entropy_example - i)

	important_a = 0
	for i in range(len(gain_entropy)):
		if gain_entropy[i] > gain_entropy[important_a]:
			important_a = i

	return important_a
# ==================================



# ======== Test decision tree ======

def accurancy_test(tree, test_array, last_correct_number, parent_node, parent_value_index):
	'''
	test the tree
	@return accuracy: float
	@parameter tree: current tree list
	@parameter test_array: test dataset
	'''

	correct_number = last_correct_number
	node = tree[0]
	key = properties_keys[node]
	count_value = 0
	p_node = parent_node
	p_value_index = parent_value_index

	for i in tree:

		if type(i) == int:
			node = i
			count_value = 0
		elif type(i) == str or type(i) == np.string_:
			value = properties_dict.get(key)[count_value]
			
			row_number = test_array.shape[0]
			for j in range(row_number):
				
				if p_node != "" and p_value_index != "":
					if test_array[j, p_node] == properties_dict.get(properties_keys[p_node])[p_value_index] and test_array[j, node] == value and test_array[j, 22] == i:
						correct_number += 1.0000
						

				elif i == test_array[j, 22] and test_array[j, node] == value:
					correct_number += 1.0000
					
			if count_value < len(properties_dict.get(key)):
				count_value += 1

		elif type(i) == list:
			p_node = node
			p_value_index = count_value
			
			
			correct_number = accurancy_test(i, test_array, correct_number, p_node, p_value_index)
			
	return correct_number


# ======test tree ==========

# Record size of taining set
sizes_of_training_set = []
for i in range(I, S+I, I):
	sizes_of_training_set.append(i)

# record correct number
correct_list = []
# calculate accuracy rate
acu_list = []

# Record final tree
final_tree = []

for i in sizes_of_training_set:
	correct = 0.0000
	increment_training_array = all_train_array[0:i, :]

	# input parameter: key_list
	# used for each training
	# training process would change the list (delete attribure from key list)
	training_keys = []
	for j in keys_list:
		training_keys.append(j)

	tree = decision_tree(increment_training_array, training_keys, np.array([]))

	final_tree = tree

	correct = accurancy_test(tree, rest_data, 0.0000, "", "")
	correct_list.append(correct)
	acu = (correct/rest_data.shape[0]) * 100.00
	format_acu = ("%.4f" % acu)
	acu_list.append(format_acu)


for i in range(len(sizes_of_training_set)):
	print "Running with ", sizes_of_training_set[i], " examples in training set.\n"
	print "Given current tree, there are", correct_list[i], "correct classifications out of 4644 possible (a success rate of", acu_list[i], "percent).\n"


# ==================================== Part 3 Output Matplotlib Graph =========================================

# x is size of training set
# y is acu
plt.plot(sizes_of_training_set, acu_list, color="k")
#plt.axis([I, S,])
#plt.xticks(np.arange(I, S, step=I))
plt.xlim(I, S)
plt.xlabel("Size of Training Set")
plt.ylabel("%Correct")
plt.show()

# ========================================================================================================

# ==================================== Part 4 Output Description of tree =================================

def description_tree(tree, parent_list):

	'''
	@return list, description the tree
	@parameter tree: list
	@parameter parent_list: list, parent-node information(str)
	'''
	tree_verb = []
	count_value = 0
	node = tree[0]
	key = properties_keys[node]

	for i in tree:
		if type(i) == int:
			node = i
			count_value = 0
		elif type(i) == str or type(i) == np.string_:
			leaf_list = []

			if i == "e":
				if len(parent_list) != 0:
					temp_le = "Attrib #" + str(node) + ": " + properties_dict.get(key)[count_value] + "; Edible."
					for j in parent_list:
						leaf_list.append(j + temp_le)
					count_value += 1


				else:
					temp_le = "Attrib #" + str(node) + ": " + properties_dict.get(key)[count_value] + "; Edible."
					leaf_list.append(temp_le)
					count_value += 1

			elif i == "p":
				if len(parent_list) != 0:
					temp_lp = "Attrib #" + str(node) + ": " + properties_dict.get(key)[count_value] + "; Poison."
					for j in parent_list:
						leaf_list.append(j + temp_lp)
					count_value += 1

				else:
					temp_lp = "Attrib #" + str(node) + ": " + properties_dict.get(key)[count_value] + "; Poison."
					leaf_list.append(temp_lp)
					count_value += 1

			for k in leaf_list:
				tree_verb.append(k)

		else:
			node_list = []
			temp_parent = "Attrib #" + str(node) + ": " + properties_dict.get(key)[count_value] + "; "
			node_list.append(temp_parent)
			node_list = description_tree(i, node_list)
			for k in node_list:
				tree_verb.append(k)

	return tree_verb


print "\n----------------------"
print " Fianl Decision Tree"
print "----------------------"

tree_verb = description_tree(final_tree, [])
for i in tree_verb:
	print i

# =========================================================================================================


# ================================== Part 5 Output Statstic ===============================================

print "\n\n----------------------"
print "       Statstic"
print "----------------------"

for i in range(len(sizes_of_training_set)):
	print "Training set size:", sizes_of_training_set[i], ", Success:", acu_list[i], "percent."


# =========================================================================================================






