from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import manhattan_distances
import numpy as np


def change_string_to_vector(string):
    # comma seperated, spaces will be ignored
    vector = []
    string = string.split('[')[1]
    string = string.split(']')[0]
    string = string.replace(r'\s', '')
    for value_string in string.split(','):
        vector.append(float(value_string))
    return np.array(vector).reshape(1, -1)


def vec_cos_sim(token_input, operation_input):
    operation_string = None
    ref_vector_string = None
    cond_value_string = None
    for opr_sign in ['==', '>=', '<=', '!=', '<>', '<', '>', '=']:
        if opr_sign in operation_input:
            ref_vector_string = operation_input.split(opr_sign)[0]
            operation_string = opr_sign
            cond_value_string = operation_input.split(opr_sign)[1]
            break

    if ref_vector_string and cond_value_string and operation_string:
        try:
            cond_value = float(cond_value_string)
            ref_vector = change_string_to_vector(ref_vector_string)
            token_vector = change_string_to_vector(token_input)
            if len(ref_vector) != len(token_vector):
                print ('len of vectors does not match')
                return False
            if operation_string == "=" or operation_string == "==":
                return cosine_similarity(token_vector, ref_vector) == cond_value
            elif operation_string == "<":
                return cosine_similarity(token_vector, ref_vector) < cond_value
            elif operation_string == ">":
                return cosine_similarity(token_vector, ref_vector) > cond_value
            elif operation_string == ">=":
                return cosine_similarity(token_vector, ref_vector) >= cond_value
            elif operation_string == "<=":
                return cosine_similarity(token_vector, ref_vector) <= cond_value
            elif operation_string == "!=" or operation_string == "<>":
                return cosine_similarity(token_vector, ref_vector) != cond_value
            else:
                return False
        except ValueError:
            # TODO raise tokenregex error
            return False

    else:
        # TODO raise tokenregex error
        print ('Problem with the operation input')


def vec_cos_dist(token_input, operation_input):
    operation_string = None
    ref_vector_string = None
    cond_value_string = None
    for opr_sign in ['==', '>=', '<=', '!=', '<>', '<', '>', '=']:
        if opr_sign in operation_input:
            ref_vector_string = operation_input.split(opr_sign)[0]
            operation_string = opr_sign
            cond_value_string = operation_input.split(opr_sign)[1]
            break

    if ref_vector_string and cond_value_string and operation_string:
        try:
            cond_value = float(cond_value_string)
            ref_vector = change_string_to_vector(ref_vector_string)
            token_vector = change_string_to_vector(token_input)
            if len(ref_vector) != len(token_vector):
                print ('len of vectors does not match')
                return False
            if operation_string == "=" or operation_string == "==":
                return cosine_distances(token_vector, ref_vector) == cond_value
            elif operation_string == "<":
                return cosine_distances(token_vector, ref_vector) < cond_value
            elif operation_string == ">":
                return cosine_distances(token_vector, ref_vector) > cond_value
            elif operation_string == ">=":
                return cosine_distances(token_vector, ref_vector) >= cond_value
            elif operation_string == "<=":
                return cosine_distances(token_vector, ref_vector) <= cond_value
            elif operation_string == "!=" or operation_string == "<>":
                return cosine_distances(token_vector, ref_vector) != cond_value
            else:
                return False
        except ValueError:
            # TODO raise tokenregex error
            return False

    else:
        # TODO raise tokenregex error
        print ('Problem with the operation input')


def vec_man_dist(token_input, operation_input):
    operation_string = None
    ref_vector_string = None
    cond_value_string = None
    for opr_sign in ['==', '>=', '<=', '!=', '<>', '<', '>', '=']:
        if opr_sign in operation_input:
            ref_vector_string = operation_input.split(opr_sign)[0]
            operation_string = opr_sign
            cond_value_string = operation_input.split(opr_sign)[1]
            break

    if ref_vector_string and cond_value_string and operation_string:
        try:
            cond_value = float(cond_value_string)
            ref_vector = change_string_to_vector(ref_vector_string)
            token_vector = change_string_to_vector(token_input)
            print(manhattan_distances(token_vector, ref_vector))
            if len(ref_vector) != len(token_vector):
                print ('len of vectors does not match')
                return False
            if operation_string == "=" or operation_string == "==":
                return manhattan_distances(token_vector, ref_vector) == cond_value
            elif operation_string == "<":
                return manhattan_distances(token_vector, ref_vector) < cond_value
            elif operation_string == ">":
                return manhattan_distances(token_vector, ref_vector) > cond_value
            elif operation_string == ">=":
                return manhattan_distances(token_vector, ref_vector) >= cond_value
            elif operation_string == "<=":
                return manhattan_distances(token_vector, ref_vector) <= cond_value
            elif operation_string == "!=" or operation_string == "<>":
                return manhattan_distances(token_vector, ref_vector) != cond_value
            else:
                return False
        except ValueError:
            # TODO raise tokenregex error
            return False

    else:
        # TODO raise tokenregex error
        print ('Problem with the operation input')
