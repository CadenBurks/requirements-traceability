"""
Analysis for part 1 of the traceability assignment
To run this analysis use 'python -m part1.analysis' in root directory

1. Data cleaning
----Below repeated for each variant----
2. Data preprocessing
3. tf-idf vectorization and cosine similarity
4. Cosine similarity sorting
5. Final analysis
"""
from .variants import variant1, variant2, variant3
from functions import tf_idf_cosine, merge_sort, transpose_with_threshold
import csv

"""
STEP 1: Data cleaning
Given requirements are read from the file.
Requirements are cleaned by removing NFR labels and white space and stored in a dictionary to prepare for preprocessing.
"""
with open("./text_files/requirements-3nfr-60fr.txt", "r") as file:
    data = file.readlines()

info = {}
for line in data:
    parts = line.split(":", 1)
    parts[0] = parts[0].replace("(Operational)", "")
    parts[0] = parts[0].replace("(Usability)", "")
    parts[0] = parts[0].replace("(Security)", "")
    parts[0] = parts[0].strip()

    if len(parts) > 1:
        parts[1] = parts[1].rstrip("\n")
        parts[1] = parts[1].strip()
        info[parts[0]] = parts[1]


variant3(info)

#region Variant 1
"""
STEP 2: Preprocessing
Variant 1 only tokenizes the NFRs and FRs.
This is important because it breaks each requirement into individual words that are required for TF-IDF vectorization
and calculating cosine similarity. This is a baseline for similarity since it is only word overlap.
The variant1 function is invoked in the tf_idf_cosine function during step 3 for simplicity.
"""
"""
STEP 3: TF-IDF Vectorization and Cosine Similarity
    First, the preprocessed text is vectorized using a TF-IDF vectorizer. This creates a matrix that has each requirement represented
with a vector. The vectors hold the weight of each item, determined by how often the item appears in an individual requirement and how
often it appears in every requirement. If a word/item appears in many requirements then its weight is low and will not impact the similarity score.
    Next, a matrix is made by applying cosine similarity. This shows the similarity between NFRs and FRs based on the vectors
from the previous step.
    Finally, a dictionary is made that holds the similarity scores between each NFR and all FRs. Only the NFR x FR relationship
is used, so no NFR x NFR or FR x FR result is held.
"""
results = tf_idf_cosine(info, variant1)

"""
STEP 4: Merge Sort
    The similarity scores for each NFR are stored in descending order using merge sort. Merge sort is used because 
of the worst case O(n log n) and the results are predictable.
    The results shown are the top n similarity scores for each NFR. These results hint that this variant
does not produce very optimal results as many of these scores are not represented in the actual trace. For example,
the top result (and the highest similarity score for every NFR) for NFR3 says that FR18 is very similar to it, but when
looking at the given trace (trace-3nfr-60fr.txt) there is no similarity as shown be the third value being 0 in "FR18,1,0,0".
"""
sorted_results = [merge_sort(results["NFR1"]), merge_sort(results["NFR2"]), merge_sort(results["NFR3"])]

while True:
    try:
        top_n = int(input("How many results to show for NFR->FR trace? (MAX 60): "))
        if 0 < top_n <= 60:
            break
    except ValueError:
        print("Invalid Input")

with open("top_n_results_variant1.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NFR", "Rank", "FR", "Similarity"])
    for i, nfr_results in enumerate(sorted_results, start=1):
        for rank, (fr, score) in enumerate(nfr_results[:top_n], start=1):
            writer.writerow([f"NFR{i}", rank, fr, f"{score:.3f}"])

"""
STEP 5: Final Analysis
    The results are transposed to match the format of the given trace results.
    
    This trace confirms the results from variant 1 are not optimal. This makes sense
as the only preprocessing done was tokenization.

    The reason that only tokenization is not optimal is because common terms like "recycled" appear in requirements and
can inflate cosine similarity despite an NFR and FR not being similar. For example, in the given trace, FR9 is traced to 
both NFR1 and NFR2 but in this trace, FR9 is only traced to NFR1 because NFR2 does not have the term "recycled".
"""
fr_view = transpose_with_threshold(results, 0.09)

with open("trace_variant1.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for fr, values in fr_view.items():
        writer.writerow([fr] + values)
#endregion

#region Variant 2
"""
STEP 2: Preprocessing
Variant 2 uses tokenization and stop word removal.
Removing stop words should help because it reduces filler words that hold no significance and 
leads to stronger word matches.
The variant2 function is invoked in the tf_idf_cosine function during step 3 for simplicity.
"""
"""
STEP 3: TF-IDF Vectorization and Cosine Similarity
    First, the preprocessed text is vectorized using a TF-IDF vectorizer. This creates a matrix that has each requirement represented
with a vector. The vectors hold the weight of each item, determined by how often the item appears in an individual requirement and how
often it appears in every requirement. If a word/item appears in many requirements then its weight is low and will not impact the similarity score.
    Next, a matrix is made by applying cosine similarity. This shows the similarity between NFRs and FRs based on the vectors
from the previous step.
    Finally, a dictionary is made that holds the similarity scores between each NFR and all FRs. Only the NFR x FR relationship
is used, so no NFR x NFR or FR x FR result is held.
"""
results = tf_idf_cosine(info, variant2)

"""
STEP 4: Merge Sort
    The similarity scores for each NFR are stored in descending order using merge sort. Merge sort is used because 
of the worst case O(n log n) and the results are predictable.
    The results shown are the top n similarity scores for each NFR. These results are not
"""
sorted_results = [merge_sort(results["NFR1"]), merge_sort(results["NFR2"]), merge_sort(results["NFR3"])]

while True:
    try:
        top_n = int(input("How many results to show for NFR->FR trace? (MAX 60): "))
        if 0 < top_n <= 60:
            break
    except ValueError:
        print("Invalid Input")

with open("top_n_results_variant2.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NFR", "Rank", "FR", "Similarity"])
    for i, nfr_results in enumerate(sorted_results, start=1):
        for rank, (fr, score) in enumerate(nfr_results[:top_n], start=1):
            writer.writerow([f"NFR{i}", rank, fr, f"{score:.3f}"])

"""
STEP 5: Final Analysis
    The results are transposed to match the format of the given trace results.
    
    This variant used tokenization and removed stop words during preprocessing.
This resulted in slightly lowered similarity scores across requirements due to the
removal of unimportant words that were contributing to similarity. The results are more
consistent but still not entirely optimal as similarity is still mostly being measured by
how similar words between requirements are, despite the intent of the wording or any synonyms.
"""
fr_view = transpose_with_threshold(results, 0.09)

with open("trace_variant2.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for fr, values in fr_view.items():
        writer.writerow([fr] + values)
#endregion

#region Variant 3
"""
STEP 2: Preprocessing
Variant 3 does tokenization, stop word removal, and lemmatization with POS tagging. This
improves similarity traces since words are reduced to their base form.
The variant3 function is invoked in the tf_idf_cosine function during step 3 for simplicity.
"""
"""
STEP 3: TF-IDF Vectorization and Cosine Similarity
    First, the preprocessed text is vectorized using a TF-IDF vectorizer. This creates a matrix that has each requirement represented
with a vector. The vectors hold the weight of each item, determined by how often the item appears in an individual requirement and how
often it appears in every requirement. If a word/item appears in many requirements then its weight is low and will not impact the similarity score.
    Next, a matrix is made by applying cosine similarity. This shows the similarity between NFRs and FRs based on the vectors
from the previous step.
    Finally, a dictionary is made that holds the similarity scores between each NFR and all FRs. Only the NFR x FR relationship
is used, so no NFR x NFR or FR x FR result is held.
"""
results = tf_idf_cosine(info, variant3)

"""
STEP 4: Merge Sort
    The similarity scores for each NFR are stored in descending order using merge sort. Merge sort is used because 
of the worst case O(n log n) and the results are predictable.
    The results shown are the top 10 similarity scores for each NFR. These results hint that this variant
does not produce very optimal results as many of these scores are not represented in the actual trace. For example,
the top result (and the highest similarity score for every NFR) for NFR3 says that FR18 is very similar to it, but when
looking at the given trace (trace-3nfr-60fr.txt) there is no similarity as shown be the third value being 0 in "FR18,1,0,0".
"""
sorted_results = [merge_sort(results["NFR1"]), merge_sort(results["NFR2"]), merge_sort(results["NFR3"])]

while True:
    try:
        top_n = int(input("How many results to show for NFR->FR trace? (MAX 60): "))
        if 0 < top_n <= 60:
            break
    except ValueError:
        print("Invalid Input")

with open("top_n_results_variant3.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NFR", "Rank", "FR", "Similarity"])
    for i, nfr_results in enumerate(sorted_results, start=1):
        for rank, (fr, score) in enumerate(nfr_results[:top_n], start=1):
            writer.writerow([f"NFR{i}", rank, fr, f"{score:.3f}"])

"""
STEP 5: Final Analysis
    The results are transposed to match the format of the given trace results.
    
    This is the most optimal variant of the 3. Lemmatization helps with matching words
that have different forms so if a word is in different forms between requirements they can
still be seen as similar. This, however, does not account for synonyms and the intent of the 
wording can only be partially accounted for.
"""
fr_view = transpose_with_threshold(results, 0.09)

with open("trace_variant3.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for fr, values in fr_view.items():
        writer.writerow([fr] + values)
#endregion