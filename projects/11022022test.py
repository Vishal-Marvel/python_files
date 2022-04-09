# Python3 program for the
# above approach

# Structure for
# Binary Tree Node
class Node:
	
	def __init__(self, data):
		
		self.data = data
		self.left = None
		self.right = None

# Function for
# dfs traversal
def dfs(root, type_t, left_leaf,
		right_leaf):

	# If node is
	# null, return
	if (not root):
		return

	# If tree consists
	# of a single node
	if (not root.left and not root.right):
		if (type_t == -1):
			print("Tree consists of a single node")
		
		elif (type_t == 0):
			left_leaf.append(root.data)
		
		else:
			right_leaf.append(root.data)

		return

	# If left child exists,
	# traverse and set type_t to 0
	if (root.left):
		dfs(root.left, 0, left_leaf,
			right_leaf)

	# If right child exists,
	# traverse and set type_t to 1
	if (root.right):
		dfs(root.right, 1, left_leaf,
			right_leaf)
	
# Function to print
# the solution
def prints(left_leaf, right_leaf):
	
	if (len(left_leaf) == 0 and
		len(right_leaf) == 0):
		return

	# Printing left leaf nodes
	print("Left leaf nodes")
	
	for x in left_leaf:
		print(x, end = ' ')
	
	print()

	# Printing right leaf nodes
	print("Right leaf nodes")
	
	for x in right_leaf:
		print(x, end = ' ')
		
	print()

# Driver code
if __name__=='__main__':

	root = Node(0)
	root.left = Node(1)
	root.right = Node(2)
	root.left.left = Node(3)
	root.left.right = Node(4)

	left_leaf = []
	right_leaf = []
	dfs(root, -1, left_leaf, right_leaf)

	prints(left_leaf, right_leaf)

# This code is contributed by pratham76
