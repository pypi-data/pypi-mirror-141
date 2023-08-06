**Distributed Random Forest**

The following algorithm description is taken directly from the H2O.ai
H2O-3 User Guide
(https://docs.h2o.ai/h2o/latest-stable/h2o-docs/index.html):

*Distributed Random Forest (DRF) is a powerful classification and
regression tool. When given a set of data, DRF generates a forest of
classification or regression trees, rather than a single classification
or regression tree. Each of these trees is a weak learner built on a
subset of rows and columns. More trees will reduce the variance. Both
classification and regression take the average prediction over all their
trees to make a final prediction, whether predicting for a class or
numeric value. In H2O, DRF maps a categorical response column\'s factors
(e.g. \"dog\", \"cat\", \"mouse\") in lexicographic order to a name
lookup array with integer indices (e.g. \"cat\"-\> 0, \"dog\"-\> 1,
\"mouse\" -\> 2).*

**{% if final_model._final_model_string == "DRF with Extremely
Randomized Trees"%}*Extremely Randomized Trees***

*In random forests, a random subset of candidate features is used to
determine the most discriminative thresholds that are picked as the
splitting rule. In extremely randomized trees (Geurts 2006), randomness
goes one step further in the way that splits are computed. As in random
forests, a random subset of candidate features is used, but instead of
looking for the most discriminative thresholds, thresholds are drawn at
random for each candidate feature, and the best of these randomly
generated thresholds is picked as the splitting rule. This usually
allows to reduce the variance of the model a bit more, at the expense of
a slightly greater increase in bias.*

*H2O supports extremely randomized trees (XRT) via
histogram\_type=\"Random\". When this is specified, the algorithm will
sample N-1 points from min...max and use the sorted list of those to
find the best split. The cut points are random rather than uniform. For
example, to generate 4 bins for some feature ranging from 0-100, 3
random numbers would be generated in this range (13.2, 89.12, 45.0). The
sorted list of these random numbers forms the histogram bin boundaries
e.g. (0-13.2, 13.2-45.0, 45.0-89.12, 89.12-100).{% endif %}*
