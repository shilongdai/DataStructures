# DataStructures
This library provides implementations of classic algorithms and datastructures. 

# Organization
The project is divided into two packages, algorithms and structure. The algorithms package contains implementations of mostly stand alone algorithms while the structure package contains data structures and algorithms that exclusively operates on them.

## Algorithms
Here is a list of algorithms under the algorithms package:

In binarySearch.py:

- standard binary search: the standard binary search. https://en.wikipedia.org/wiki/Binary_search_algorithm
- first occurence binary search: the standard binary search except that it finds the first element that matches the search key.

In expression.py:

- Shunting yard algorithm: Dijkstra's algorithm for converting infix to postfix notation. https://en.wikipedia.org/wiki/Shunting-yard_algorithm

- Dijkstra's two stack algorithm: Dijkstra's algorithm for interpreting postfix expressions.

In problemSolver.py:

- A* algorithm: A path finding algorithm. https://en.wikipedia.org/wiki/A*_search_algorithm
- A* algorithm adapted to the 8-puzzle problem: https://www.cs.princeton.edu/courses/archive/spr10/cos226/assignments/8puzzle.html

In sort.py:

- Selection sort: https://en.wikipedia.org/wiki/Selection_sort
- Insertion sort: https://en.wikipedia.org/wiki/Insertion_sort
- Shell sort: https://en.wikipedia.org/wiki/Shellsort
- Variations of Merge sort: https://en.wikipedia.org/wiki/Merge_sort
- Inversion count: Count the number of inversions with modified merge sort
- Variations of Quick sort: Including standard quick sort, 3-way quick sort, and sampling quick sort. https://en.wikipedia.org/wiki/Quicksort
- Heap sort: https://en.wikipedia.org/wiki/Heapsort
- Select kth: select the kth element in order. Based on the quick sort partition.

## Structure
Here is a list of implemented data structures and algorithms that operates on them:

In linkedList.py:

- Linked list: https://en.wikipedia.org/wiki/Linked_list
- Linked stack: Stack implemented with a Linked List.
- Linked queue: Queue implemented with a Linked List.

In unionFind.py: https://en.wikipedia.org/wiki/Disjoint-set_data_structure

- Quick Find: Disjoint set implemented with array like data structure. O(1) find.
- Quick Union: Disjoint set implemented with parent link tree.
- Balanced Quick Union: Disjoint set implemented with parent link tree and balancing on union. O(log(N)) efficiency for find and union.
- Path Compression Quick Union: Disjoint set implemented with parent link tree and augmented with path compression.
- Balanced Path Compression Quick Union: Disjoint set implemented with parent link tree with balancing and path compression. almost amortized O(1) efficiency on find and union.

In symbolTable.py:

- Binary Search Tree: Standard BST. https://en.wikipedia.org/wiki/Binary_search_tree
- Red & Black Tree: Balanced BST using 2-3 representation. https://en.wikipedia.org/wiki/Red%E2%80%93black_tree
- Separate Chaining Hash Table: Hash table that resolve collision by chaining them in a list. https://en.wikipedia.org/wiki/Hash_table#Separate_chaining
- Open Address Hash Table: Hash table that resolve collision with linear probing. https://en.wikipedia.org/wiki/Hash_table#Open_addressing

In heap.py:

- Binary Heap: An implementation of a priority queue with binary heap. https://en.wikipedia.org/wiki/Binary_heap

In graph.py:

- Undirected Graph: https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Undirected_graph
- Directed Graph: https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph
- Undirected Weighted Graph: https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Weighted_graph
- Directed Weighted Graph: https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Weighted_graph
- Depth First Search: https://en.wikipedia.org/wiki/Depth-first_search
- Breadth First Search: https://en.wikipedia.org/wiki/Breadth-first_search
- Undirected Connected Components: https://en.wikipedia.org/wiki/Component_(graph_theory)
- Undirected Cycle Detection: https://en.wikipedia.org/wiki/Cycle_(graph_theory)
- Directed Cycle Detection: https://en.wikipedia.org/wiki/Cycle_(graph_theory)
- Biparte Detection: https://en.wikipedia.org/wiki/Bipartite_graph
- Topological Ordering: https://en.wikipedia.org/wiki/Topological_sorting
- Strongly Connected Components(Kosaraju's algorithm): https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
- Prim's Algorithm(Lazy): https://en.wikipedia.org/wiki/Prim%27s_algorithm
- Kruskal's Algorithm: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
- Dijkstra's Shortest Path: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Topological Acyclic Shortest Path: https://en.wikipedia.org/wiki/Topological_sorting#Application_to_shortest_path_finding
- Bellman Ford Shortest path: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm

# Usage
All of the components are tested. However, they are not tested to rigorous production standards. Data structures such as the linked list and symbolTables have interfaces like the standard python list and dictionary.
