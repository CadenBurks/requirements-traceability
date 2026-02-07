# requirements-traceability

## Running the analyses
1. Make sure you are in the root directory of the repository
2. Run either 'python -m part_1.analysis' or 'python part_2.analysis'
4. The output in the terminal will show the TF-IDF scores followed by the cosine similarity scores.
5. Each variant will ask for the top N results that you want to see after sorting.
6. Preprocessing and Merge Sort results can be found in the following folders: 'part_1_results', 'part_2_results'

## Part 1 (Given requirements)
**Optimal Variant -> Variant 3** 

Why Variant 3 is the optimal one: 
This is the most effective variant of the 3 that were tested. Lemmatization helps with matching words that have different forms so if a word is in different forms between requirements they can still be seen as similar, and POS tagging helps lemmatize words using the proper form like nouns, verbs, etc. The addition word net expansion results in lower similarity scores but the similarities are being tracked by the meaning of the words more than the other variants. This is the most optimal variant because we want to compare the meaning behind the words in the functional requirements vs. The non-functional requirements. The meaning behind the words is more important compared to the words being similar because the requirements are for one system and show how closely related the functional and non-functional requirements are to each other.

Additional analysis can be found in the comments of part_1/analysis.py

## Part 2 (Requirements taken from Zoom release notes)
**Optimal Variant -> Variant 2**

Why Variant 2 is the optimal one: 

The results here show stronger similarity scores. Lemmatization helps with matching words that have different forms so if a word is in different forms between requirements, they can still be seen as similar, and POS tagging helps lemmatize words using the proper form like nouns, verbs, etc. This variant is the most optimal because we are looking at how similar the functional requirements are compared to the non-functional requirements. The similarity between the words is especially important because the requirements come from different systems. Comparing how the wording aligns across functional and non‑functional requirements from these systems provides more meaningful insights.

Additional analysis can be found in the comments of part_2/analysis.py

## Conclusion
Part 1 and Part 2 differ in how the results are produced. Variant 3 in Part 1 was the most optimal, while Variant 2 in Part 2 was the most optimal due to similarity scores. The similarity scores were higher because the preprocessing focused on word requirements rather than their specific meanings. By using Zoom’s release notes in Part 2, there were more features than a single direct topic, which introduced more terminology. Due to this, the similarity scores were much lower compared to Part 1. Focusing on requirements is often better than focusing on meaning because traceability is about linking rather than interpretation.
