"""
Functions used in tracing process
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tf_idf_cosine(info, output_path, variant_function):
    keys, preprocessed_text = variant_function(info, output_path)
    vectorizer = TfidfVectorizer()

    tf_idf_matrix = vectorizer.fit_transform(preprocessed_text)
    feature_names = vectorizer.get_feature_names_out()
    print("TF-IDF RESULT:")
    for req_idx in range(tf_idf_matrix.shape[0]):
        row = tf_idf_matrix[req_idx]
        for col_idx, value in zip(row.indices, row.data):
            if req_idx in [0, 1, 2]:
                print(f"NFR {req_idx + 1}, Word '{feature_names[col_idx]}': {value:.3f}")
            else:
                print(f"FR {req_idx - 2}, Word '{feature_names[col_idx]}': {value:.3f}")

    similarity = cosine_similarity(tf_idf_matrix)
    print("COSINE SIMILARITY (NFR to FR)")
    for i in range(3):
        for j in range(3, len(keys)):
            print(f"{keys[i]} -> {keys[j]}: {similarity[i][j]:.3f}")

    nfr_indices = [0, 1, 2]
    result = {
        keys[0]: [],
        keys[1]: [],
        keys[2]: [],
    }

    for i in nfr_indices:
        for j in range(3, len(keys)):
            result[keys[i]].append((keys[j], similarity[i][j]))
    return result

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