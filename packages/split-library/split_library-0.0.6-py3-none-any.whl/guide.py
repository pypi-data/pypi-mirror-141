def split_help(option=0):
    if option == 0:
        print('''split_library guide
------------
use help(selection) to see details


1. unlimited_homogeneous_veh_split(graph_distance_matrix)
2. build_split_solution_unlimited_homogeneous(pred, p)
3. limited_homogeneous_veh_split(graph_distance_matrix, n_veh)
4. build_split_solution_limited_veh(pred,p)
5. ordered_heterogeneous_split(graph_distance_matrices, veh_order)
6. heterogeneous_split(all_veh, graph_distance_matrices)
7. build_split_solution_heterogeneous(pred, p, best_veh, veh_order)''')
    elif option == 1:
        print('''1. unlimited_homogeneous_veh_split(graph_distance_matrix)

Input: 

graph_distance_matrix: An (n x n) array where A[i][j] denotes the cost of the arc from i to j and n is the number of location including depot.
If an arc from i to j is infeasible, A[i][j] = infinity
A[i][i] = infinity

Output:

Predecessor array and cost array.
Cost[i] denotes the cheapest cost to reach location i
Pred[i] denotes the location that have to be visited right before i''')
    elif option == 2:
        print('''2. build_split_solution_unlimited_homogeneous(pred, p)

Input:

Pred (predecessor) array and cost array from unlimited_homogeneous_veh_split function

Output:

A dictionary contains splitted tour, total cost and check point of last visited node of each vehicle
''')
    elif option == 3:
        print('''3. limited_homogeneous_veh_split(graph_distance_matrix, n_veh)

Input:

An (n x n) array where A[i][j] denotes the cost of the arc from i to j and n is the number of location including depot.
If an arc from i to j is infeasible, A[i][j] = infinity
A[i][i] = infinity

n_veh is the limited number of vehicle

Output:

Predecessor array and cost array of 2-dim
Cost[k][i] denotes the cheapest cost to reach location i using exactly k vehicle
Pred[k][i] denotes the location that have to be visited right before i using exactly k vehicle''')
    elif option == 4:
        print('''4. build_split_solution_limited_veh(pred,p)

Input:

Pred (predecessor) array and cost array from limited_homogeneous_veh_split and ordered_heterogeneous_split function

Output:		

A dictionary contains splitted tour, total cost and check point of last visited node of each vehicle''')
    elif option == 5:
        print('''5. ordered_heterogeneous_split(graph_distance_matrices, veh_order)

Input:

An (m x n x n) array where A[k][i][j] denotes the cost of the arc from i to j using the vehicle of type k; and n is the number of location including depot.
If an arc from i to j is infeasible, A[i][j] = infinity
A[i][i] = infinity

veh_order is the order of vehicle naming by their type (1,2,3...)

Output:	

Predecessor array and cost array of 2-dim
Cost[k][i] denotes the cheapest cost to reach location i using exactly k vehicle
Pred[k][i] denotes the location that have to be visited right before i using exactly k vehicle
''')
    elif option == 6:
        print('''6. heterogeneous_split(all_veh, graph_distance_matrices)

Input:

An (m x n x n) array where A[k][i][j] denotes the cost of the arc from i to j using the vehicle of type k; and n is the number of location including depot.
If an arc from i to j is infeasible, A[i][j] = infinity
A[i][i] = infinity

all_veh is a list of vehicle naming by their type (1,2,3...) in any order

Output:	

Predecessor array and cost array of 2-dim
Cost[k][i] denotes the cheapest cost to reach location i using exactly k vehicle
Pred[k][i] denotes the location that have to be visited right before i using exactly k vehicle
Number of vehicle used
Order of used vehicle''')
    elif option == 7:
        print('''7. build_split_solution_heterogeneous(pred, p, best_veh, veh_order)

Pred (predecessor) array, cost array, number of vehicle used and their order from heterogeneous_split function

Output:		

A dictionary contains splitted tour, total cost, all vehicles used respectively and check point of last visited node of each vehicle''')
