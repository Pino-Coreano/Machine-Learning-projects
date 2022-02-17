#!/usr/bin/env python3
# __author__ = "Suo"

import sys
import copy
import os
import math

'''
some important global variables used in this program
@variable: feature_dimension: int, store dimension load from file
@variable: list_points: list, store points list load fron file
@variable: list_path: list, list of path of the node
@variable: list_node: list, list of leaves of the tree
'''

# ========================== Part 1: Get parameter from command line ==================================
# read user input from command line
# fisrt parameter is the name of file, which have same path with this program
param_filename = sys.argv[1]
# second parameter is the size of split size S
param_split_size = int(sys.argv[2])

'''
function: load the file
		  get the dimension of the loaded data, storeed into feature_dimension
		  get the points list in the load file, storeed into list_points
@param filename: str, name of the user input file
@return reture two variables
		v-1: feature_dimension: int
		v-2: list_points: list
'''


def load_file(filename):
    # prefix of load_file path
    file_path = os.path.dirname(__file__) + "inputData/"
    file_name = file_path + str(filename)
    # load the chooed file
    file_load = open(str(file_name), "r")
    file_readlines = file_load.readlines()

    for i in range(len(file_readlines)):
        file_readlines[i] = file_readlines[i].strip("\n")
        file_readlines[i] = file_readlines[i].split(" ")

    list_file = file_readlines

    file_load.close()

    # feature dimension in the load file
    feature_dimension = (list_file[0][0])
    feature_dimension = int(feature_dimension)

    # store points from file into list
    list_points = copy.copy(list_file)
    list_points.remove(list_points[0])

    return feature_dimension, list_points


load_file(param_filename)
feature_dimension = load_file(param_filename)[0]
list_points = load_file(param_filename)[1]

# =====================================================================================================

# ========================== Part 2: Build K_D Tree ==================================

'''
define class Node, store the data as an object to build a tree
'''


class Node(object):
    def __init__(self, data):
        self.root = data
        self.lchild = None
        self.rchild = None

    '''
    function: get the boundary of the leaf node
    @param list, node of the label
    @return list, boundary of the node
    '''

    def boundary_box(self):
        # store min and max value in each demision
        min_list = []
        max_list = []
        boundary = []
        data_points = self.root
        # determine if the node is leaf
        if len(data_points) != 0:

            if type(data_points) != str:
                # find the min and max in each dimension in the list of poits/ a point
                for i in range(feature_dimension):
                    # sort data by demision_i
                    data_bounding = copy.copy(data_points)
                    data_bounding.sort(key=lambda elem: elem[i])
                    min_list.append(data_bounding[0][i])
                    max_list.append(data_bounding[len(data_bounding) - 1][i])
                    boundary = [min_list, max_list]

            return boundary


'''
@param X: list, data points load from file
@param d: int, depth of tree level
@return Tree: Node, node of the tree 
'''


def build_tree(X, d):
    if param_split_size >= len(X):
        return Node(X)

    elif len(X) == 0:
        return Node(X)

    else:
        # data points sorted by d-dimension
        divede_dimension = int(d % feature_dimension)
        X_sorted = sorted(X, key=lambda x: x[divede_dimension])

        median_x = int((len(X_sorted) - 1) / 2)
        X_left = []
        X_right = []
        for i in range(len(X_sorted)):
            if X_sorted[i][divede_dimension] <= X_sorted[median_x][divede_dimension]:
                X_left.append(X_sorted[i])
            else:
                X_right.append(X_sorted[i])

        N = Node(X[median_x][divede_dimension])
        N.lchild = build_tree(X_left, d + 1)
        N.rchild = build_tree(X_right, d + 1)
        return N


# store path of every nodes
list_path = []
# store points in every nodes
list_leaves = []
# store boundary of every leaves-nodes
boundary_box = []

'''
function: print tree leaves
@param label: str, path of current node
@param head: Node, node of the tree
'''


def print_tree(label, head):
    label_self = label
    if type(head.root) != str and label_self != None and len(head.root) != 0:
        # get current path of the node
        list_path.append(label_self)
        # get the points in the node
        list_leaves.append(head.root)
        # get the boundary of the node
        boundary = head.boundary_box()

        boundary_box.append(boundary)

    # determine if current node has left child
    if head.lchild != None:
        # remember the path of the child-node
        label_self = label + "L"

        print_tree(label_self, head.lchild)

    # determine if current node has right child
    if head.rchild != None:
        # remember the path of the child-node
        label_self = label + "R"
        print_tree(label_self, head.rchild)

    return


# ================ User determine print the tree or not =====================

tree = build_tree(list_points, 0)
print_tree("", tree)

in_print = input("Print tree leaves? (Enter Y for yes, anything else for no): ")
if in_print == "y" or in_print == "Y":
    print("\n--------------------------------------\n")
    for i in range(len(list_leaves)):
        print(str(i) + ".", list_path[i] + ":" + " Boundary Box: ", boundary_box[i])
        print("Data in leaf: ", list_leaves[i])
    print("\n--------------------------------------\n")

# ===========================================================================


# ================ User determine test the tree or not =====================

in_print = input("Test data? (Enter Y for yes, anything else to quit): ")
if in_print == "y" or in_print == "Y":
    test_file = input("Name of data-file: ")
    print("\n--------------------------------------\n")

    load_file(test_file)

    # feature dimension in the load file
    test_dimension = load_file(test_file)[0]

    # store points from file into list
    test_points = load_file(test_file)[1]

    if test_dimension == feature_dimension:

        '''
        function: calculate the distance of test points and the points in the tree
        @param tree: list, tree node
        @param point: list, test point traveled on the leaf node
        @retuen distance: float, distance between the test point and the tree leaf node
                nearest_point: list, the nearest point
        '''


        def e_distance(tree, point):
            nearest_point = []
            nearest = 100.0000
            node = tree

            for i in node:
                if i == node:
                    nearest_point = i
                    nearest = float("%.6f" % 0.000000)

                else:
                    distance = 0
                    for d in range(test_dimension):
                        distance += (float(i[d]) - float(point[d])) ** 2
                    distance = math.sqrt(distance)
                    if distance < nearest:
                        nearest = distance
                        nearest_point = i

            return nearest_point, nearest


        '''
        function: test the tree with data from test file
        @param data: list, single point in the test_points list
        @param tree: tree, K_D tree
        @param depth: int, depth of node
        '''


        def testTree(data, tree, depth):

            # d is the divide demision of current depth
            d = int(depth % test_dimension)

            if type(tree.root) == str:
                if i[d] <= tree.root:
                    testTree(data, tree.lchild, depth + 1)
                else:
                    testTree(data, tree.rchild, depth + 1)

            elif len(tree.root) == 0:
                print(data, "has no nearest neighbor (in an empty set).")


            else:
                e_distance(tree.root, data)
                nearest_neighbor = e_distance(tree.root, data)[0]
                distance = float(e_distance(tree.root, data)[1])
                distance = ("%.6f" % distance)
                print(data, "is in the set: ", tree.root)
                print("Nearest neighbor: ", nearest_neighbor, "(distance = " + str(distance) + ")\n")


        # test the points in the test set
        for i in test_points:
            testTree(i, tree, 0)

    else:
        print("Test file have different dimension with tree")
    print("--------------------------------------\n")

# ===========================================================================

print("Goodbye.")

# =====================================================================================
