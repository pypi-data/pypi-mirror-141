import math
import numpy as np
from numba import njit, types
from numba.typed import Dict
from itertools import permutations


@njit(fastmath=True)
def unlimited_homogeneous_veh_split(graph_distance_matrix):
    n_location = len(graph_distance_matrix)
    p = np.asarray([math.inf for i in range(n_location)], dtype='float64')
    p[0] = 0
    pred = np.asarray([-1 for i in range(n_location)], dtype='int64')
    for t in range(n_location):
        i = t + 1
        while i < n_location and graph_distance_matrix[t][i] < math.inf:
            if p[t] + graph_distance_matrix[t][i] < p[i]:
                p[i] = p[t] + graph_distance_matrix[t][i]
                pred[i] = t
            i += 1
    return pred, p


def build_split_solution_unlimited_homogeneous(pred, p):
    res = {'total cost': p[-1]}
    checkpoint = []
    location = len(pred) - 1
    checkpoint.append(location)
    while location != 0:
        checkpoint.append(pred[location])
        location = pred[location]
    checkpoint = checkpoint[-1::-1]
    res['checkpoint'] = checkpoint
    split_tour = []
    for i in range(1, len(checkpoint)):
        temp_list = []
        temp_point = checkpoint[i - 1]
        for j in range(checkpoint[i - 1] + 1, checkpoint[i] + 1):
            temp_list.append(j)
        split_tour.append(temp_list)
    res['tour'] = split_tour
    return res


@njit(fastmath=True)
def limited_homogeneous_veh_split(graph_distance_matrix, n_veh):
    n_location = len(graph_distance_matrix)
    p = np.asarray([[math.inf for i in range(n_location)] for i in range(n_veh + 1)], dtype='float64')
    p[0][0] = 0
    pred = np.asarray([[-1 for i in range(n_location)] for i in range(n_veh + 1)], dtype='int64')
    for k in range(1, n_veh + 1):
        for t in range(k - 1, n_location):
            i = t + 1
            while i < n_location and graph_distance_matrix[t][i] < math.inf:
                if p[k - 1][t] + graph_distance_matrix[t][i] < p[k][i]:
                    p[k][i] = p[k - 1][t] + graph_distance_matrix[t][i]
                    pred[k][i] = t
                i += 1
    return pred, p


def build_split_solution_limited_veh(pred, p):
    min_cost = math.inf
    optimal_n_veh = math.inf
    for i in range(len(p)):
        if p[i][-1] < min_cost:
            min_cost = p[i][-1]
            optimal_n_veh = i
    res = {'total cost': min_cost, 'n_veh': optimal_n_veh}
    checkpoint = []
    location = len(pred[0]) - 1
    checkpoint.append(location)
    for count in range(optimal_n_veh, 0, -1):
        checkpoint.append(pred[count][location])
        location = pred[count][location]
    checkpoint = checkpoint[-1::-1]
    res['checkpoint'] = checkpoint
    split_tour = []
    for i in range(1, len(checkpoint)):
        temp_list = []
        temp_point = checkpoint[i - 1]
        for j in range(checkpoint[i - 1] + 1, checkpoint[i] + 1):
            temp_list.append(j)
        split_tour.append(temp_list)
    res['tour'] = split_tour
    return res


@njit(fastmath=True)
def ordered_heterogeneous_split(graph_distance_matrices, veh_order):
    n_location = len(graph_distance_matrices[0])
    n_veh = len(veh_order)
    p = np.asarray([[math.inf for i in range(n_location)] for i in range(n_veh + 1)], dtype='float64')
    p[0][0] = 0
    pred = np.asarray([[-1 for i in range(n_location)] for i in range(n_veh + 1)], dtype='int64')
    best_cost = math.inf
    best_veh = 0
    for k in range(1, n_veh + 1):
        for t in range(k - 1, n_location):
            i = t + 1
            while i < n_location and graph_distance_matrices[veh_order[k - 1] - 1][t][i] < math.inf:
                if p[k - 1][t] + graph_distance_matrices[veh_order[k - 1] - 1][t][i] < p[k][i]:
                    p[k][i] = p[k - 1][t] + graph_distance_matrices[veh_order[k - 1] - 1][t][i]
                    pred[k][i] = t
                i += 1
        if p[k][-1] < best_cost:
            best_cost = p[k][-1]
            best_veh = k
    return pred, p


def permutation(veh_list):
    return list(set(list(permutations(veh_list))))


def all_bin(n):
    res = []
    for i in range(n):
        res.append(bin(i)[2:])
    return res


def find_all_subset(alist):
    res = []
    n = 2 ** len(alist)
    for _ in all_bin(n):
        mem = []
        for i in range(len(_) - 1, -1, -1):
            if _[i] == '1':
                mem.append(alist[len(alist) - len(_) + i])
        res.append(tuple(mem))
    return res


def find_all_key(alist):
    res = set()
    for _ in find_all_subset(alist):
        for __ in permutation(_):
            res.add(__)
    res = list(res)
    res.sort(key=lambda x: len(x))
    return res


def sync(alist):
    res = np.zeros((len(alist), len(alist[-1])), dtype="int64")
    for i in range(len(alist)):
        for j in range(len(alist[-1]) - 1, len(alist[-1]) - len(alist[i]) - 1, -1):
            res[i][j] = alist[i][len(alist[-1]) - j - 1]
    return res


@njit(fastmath=True)
def mapping(array):
    res = 0
    for i in range(len(array)):
        res += array[-1 - i] * 10 ** i
    return int(res)


def create_variable(veh_order):
    global float_array, int_array, tuple_type
    float_array = types.float64[:, :]
    int_array = types.int64[:, :]
    tuple_type = types.UniTuple(types.float64, len(veh_order))


@njit(fastmath=True, cache=True)
def heterogeneous_split(key_list, graph_distance_matrices):
    n_location = len(graph_distance_matrices[0])
    n_veh = len(key_list[-1])
    mem_p = Dict.empty(
        key_type=types.int64,
        value_type=float_array,
    )
    mem_pred = Dict.empty(
        key_type=types.int64,
        value_type=int_array,
    )
    p = np.full((n_veh + 1, n_location), np.inf, dtype='float64')
    p[0][0] = 0
    pred = np.full((n_veh + 1, n_location), -1, dtype='int64')
    for _ in key_list:
        mem_p[mapping(_)] = p
    for _ in key_list:
        mem_pred[mapping(_)] = pred
    best_cost = 10 ** 9
    best_veh = 0
    for _ in key_list[1:]:
        __ = np.concatenate((np.zeros(1), _[1:]), axis=0)
        mem_p[mapping(_)] = mem_p[mapping(__)]
        mem_pred[mapping(_)] = mem_pred[mapping(__)]
        k = 0
        for item in _:
            if item != 0:
                k += 1
        for t in range(k - 1, n_location):
            i = t + 1
            while i < n_location and graph_distance_matrices[_[-1] - 1][t][i] < math.inf:
                if mem_p[mapping(_)][k - 1][t] + graph_distance_matrices[_[-1] - 1][t][i] < mem_p[mapping(_)][k][i]:
                    mem_p[mapping(_)][k][i] = mem_p[mapping(_)][k - 1][t] + graph_distance_matrices[_[-1] - 1][t][i]
                    mem_pred[mapping(_)][k][i] = t
                i += 1

        for i in range(len(mem_p[mapping(_)])):
            if mem_p[mapping(_)][i][-1] < best_cost:
                best_cost = mem_p[mapping(_)][i][-1]
                best_veh = i
                p, pred = mem_p[mapping(_)], mem_pred[mapping(_)]

    return p, pred, best_cost, best_veh


@njit(fastmath=True)
def unlimited_heterogeneous_split(graph_distance_matrices):
    n_location = len(graph_distance_matrices[0])
    p = np.asarray([math.inf for i in range(n_location)], dtype='float64')
    p[0] = 0
    pred = np.asarray([-1 for i in range(n_location)], dtype='int64')
    for t in range(n_location):
        i = t + 1
        for graph in graph_distance_matrices:
            while i < n_location and graph[t][i] < math.inf:
                if p[t] + graph[t][i] < p[i]:
                    p[i] = p[t] + graph[t][i]
                    pred[i] = t
                i += 1
    return pred, p
