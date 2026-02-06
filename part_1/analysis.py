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
from methods.variants import variant1, variant2, variant3
from methods.functions import tf_idf_cosine, merge_sort, transpose_with_threshold
from pathlib import Path
import csv

results_directory = Path("part_1_results")
results_directory.mkdir(exist_ok=True)


"""
STEP 1: Data cleaning
Given requirements are read from the file.
Requirements are cleaned by removing NFR categories and removing white space and stored in a dictionary to prepare for preprocessing.
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

#region Variant 1
"""
STEP 2: Preprocessing
Variant 1 tokenizes and removes stop words.
This is important because it breaks each requirement into individual words that are required for TF-IDF vectorization
and calculating cosine similarity. It also removes filler words that may appear like "the", "and", etc.
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
    The results shown are the top n similarity scores for each NFR.
"""
sorted_results = [merge_sort(results["NFR1"]), merge_sort(results["NFR2"]), merge_sort(results["NFR3"])]

while True:
    try:
        top_n = int(input("VARIANT 1: How many results to show for NFR->FR trace? (MAX 60): "))
        if 0 < top_n <= 60:
            break
    except ValueError:
        print("Invalid Input")

full_path = results_directory / Path("top_n_results_variant1.csv")
with full_path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NFR", "Rank", "FR", "Similarity"])
    for i, nfr_results in enumerate(sorted_results, start=1):
        for rank, (fr, score) in enumerate(nfr_results[:top_n], start=1):
            writer.writerow([f"NFR{i}", rank, fr, f"{score:.3f}"])

"""
STEP 5: Final Analysis
    The results are transposed to match the format of the given trace results.
    
    The similarity traces are not as accurate for this variant since tokenization and removing stop words do
not account for words being in different forms and for words that have synonyms across documents.
"""
fr_view = transpose_with_threshold(results, 0.09)

full_path = results_directory / Path("trace_variant1.csv")
with full_path.open("w", newline="") as file:
    writer = csv.writer(file)
    for fr, values in fr_view.items():
        writer.writerow([fr] + values)
#endregion

#region Variant 2
"""
STEP 2: Preprocessing
Variant 2 uses tokenization, stop word removal, and lemmatization using POS tags.

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
    The results shown are the top n similarity scores for each NFR.
"""
sorted_results = [merge_sort(results["NFR1"]), merge_sort(results["NFR2"]), merge_sort(results["NFR3"])]

while True:
    try:
        top_n = int(input("VARIANT 2: How many results to show for NFR->FR trace? (MAX 60): "))
        if 0 < top_n <= 60:
            break
    except ValueError:
        print("Invalid Input")

full_path = results_directory / Path("top_n_results_variant2.csv")
with full_path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NFR", "Rank", "FR", "Similarity"])
    for i, nfr_results in enumerate(sorted_results, start=1):
        for rank, (fr, score) in enumerate(nfr_results[:top_n], start=1):
            writer.writerow([f"NFR{i}", rank, fr, f"{score:.3f}"])

"""
STEP 5: Final Analysis
    The results are transposed to match the format of the given trace results.
    
    The results here show stronger similarity scores than the previous variant. Lemmatization helps with 
matching words that have different forms so if a word is in different forms between requirements they can
still be seen as similar, and POS tagging helps lemmatize words using the proper form like nouns, verbs, etc. 
This, however, does not account for synonyms and the intent of the wording can only be partially accounted for.
"""
fr_view = transpose_with_threshold(results, 0.11)

full_path = results_directory / Path("trace_variant2.csv")
with full_path.open("w", newline="") as file:
    writer = csv.writer(file)
    for fr, values in fr_view.items():
        writer.writerow([fr] + values)
#endregion

#region Variant 3
"""
STEP 2: Preprocessing
Variant 3 does tokenization, stop word removal, lemmatization with POS tagging, and word net expansion. This
improves similarity traces by reducing words to their base form and also providing synonyms for significant words.
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
    The results shown are the top n similarity scores for each NFR.
"""
sorted_results = [merge_sort(results["NFR1"]), merge_sort(results["NFR2"]), merge_sort(results["NFR3"])]

while True:
    try:
        top_n = int(input("VARIANT 3: How many results to show for NFR->FR trace? (MAX 60): "))
        if 0 < top_n <= 60:
            break
    except ValueError:
        print("Invalid Input")

full_path = results_directory / Path("top_n_results_variant3.csv")
with full_path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NFR", "Rank", "FR", "Similarity"])
    for i, nfr_results in enumerate(sorted_results, start=1):
        for rank, (fr, score) in enumerate(nfr_results[:top_n], start=1):
            writer.writerow([f"NFR{i}", rank, fr, f"{score:.3f}"])

"""
STEP 5: Final Analysis
    The results are transposed to match the format of the given trace results.
    
    This is the most effective variant of the 3 that were tested. Lemmatization helps with matching words
that have different forms so if a word is in different forms between requirements they can
still be seen as similar, and POS tagging helps lemmatize words using the proper form like nouns, verbs, etc. 
The addition word net expansion results in lower similarity scores but the similarities are being traced by the meaning
of the words more than the other vairants.
"""
fr_view = transpose_with_threshold(results, 0.14)

full_path = results_directory / Path("trace_variant3.csv")
with full_path.open("w", newline="") as file:
    writer = csv.writer(file)
    for fr, values in fr_view.items():
        writer.writerow([fr] + values)
#endregion