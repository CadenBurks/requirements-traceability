"""
Functions used in tracing process
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tf_idf_cosine(info, variant_function):
    keys, preprocessed_text = variant_function(info)
    vectorizer = TfidfVectorizer()

    tf_idf_matrix = vectorizer.fit_transform(preprocessed_text)

    similarity = cosine_similarity(tf_idf_matrix)

    nfr_indices = [0, 1, 2]
    result = {
        keys[0]: [],
        keys[1]: [],
        keys[2]: [],
    }
    for i in nfr_indices:
        #print(f"NFR{i+1}")
        for j in range(3, len(keys)):
            #print(f"{keys[j]}, {similarity[i][j]}")
            result[keys[i]].append((keys[j], similarity[i][j]))
    return result

# def apply_threshold(trace: list, threshold: float):
#     result = []
#     for x in trace:
#         if x[1] > threshold:
#             result.append((x[0], 1, x[1]))
#         else:
#             result.append((x[0], 0, x[1]))
#     return result

def transpose_with_threshold(results, threshold=0.14):
    frs_result = {}
    nfr_keys = list(results.keys())

    all_frs = []
    for res in results[nfr_keys[0]]:
        all_frs.append(res[0])

    for fr in all_frs:
        frs_result[fr] = []
        for nfr in nfr_keys:
            score = 0
            for res in results[nfr]:
                if res[0] == fr:
                    score = res[1]
                    break
            frs_result[fr].append(1 if score > threshold else 0)
    
    return frs_result

def merge(left_array, right_array):
    """
    Helper function for merge_sort
    
    param - left_array: Left half of array
    param - right_array: Right half of array

    return - merged: Contents of left and right array sorted in descending order
    """
    merged = []
    i, j = 0, 0

    while i < len(left_array) and j < len(right_array):
        if left_array[i][1] >= right_array[j][1]:
            merged.append(left_array[i])
            i += 1
        else:
            merged.append(right_array[j])
            j += 1
    
    while i < len(left_array):
        merged.append(left_array[i])
        i += 1
    while j < len(right_array):
        merged.append(right_array[j])
        j += 1
    
    return merged

def merge_sort(arr):
    """
    Docstring for merge_sort
    
    param - arr: Array to be sorted

    return - arr, sorted in descending order.
           - BASE CASE: arr, unchanged if there is only one item.
           - BASE CASE: [], empty array if there is an empty input.
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        left_sorted = merge_sort(left)
        right_sorted = merge_sort(right)

        return merge(left_sorted, right_sorted)
    elif len(arr) == 1:
        return arr
    else:
        return []