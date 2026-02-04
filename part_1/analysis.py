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
from .variants import variant1
from functions import tf_idf_cosine, merge_sort

"""
STEP 1: Data cleaning
Given requirements are read from the file.
Requirements are cleaned by removing any labels and white space and stored in a dictionary to prepare for preprocessing.
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
Variant 1 only tokenizes the NFRs and FRs.
This is important because it breaks each requirement into individual words that are required for TF-IDF vectorization
and calculating cosine similarity.
This variant1 function invoked in the tf_idf_cosine function during step 3 for simplicity.
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
The similarity scores for each NFR are stored in descending order using merge sort.
Merge sort is used because of the worst case O(n log n) and the results are predictable.
"""
nfr1_trace = merge_sort(results["NFR1"])
nfr2_trace = merge_sort(results["NFR2"])
nfr3_trace = merge_sort(results["NFR3"])

print(nfr1_trace)
#endregion