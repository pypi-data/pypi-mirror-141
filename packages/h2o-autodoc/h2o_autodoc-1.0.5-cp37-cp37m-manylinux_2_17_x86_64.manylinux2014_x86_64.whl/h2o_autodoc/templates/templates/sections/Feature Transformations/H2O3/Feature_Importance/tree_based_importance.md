Feature importance is determined by calculating the relative influence
of each variable: whether that variable was selected to split on during
the tree building process, and how much the squared error (over all
trees) improved (decreased) as a result.

Whenever H2O-3 splits a node, based on a numeric or categorical feature,
the feature's attributed reduction in squared error is the difference in
squared error between that node and its children nodes. The squared
error for each individual node is the reduction in variance of the
response value within that node. (The calculation assumes an unbiased
estimator, i.e., $SE = MSE*N = VAR*N)$:

Variance Equation:

$$VAR = \frac{1}{N}\sum_{i = 0}^{N}{(y_{i} - \overline{y})^{2}}$$

Squared Error Equation:

$$SE = VAR \times N = \lbrack\frac{1}{N} \times \sum_{i = 0}^{N}{y_{i}^{2} - N \times {\overline{y}}^{2}}\rbrack \times N = \lbrack\sum_{i = 0}^{N}{\frac{y_{i}^{2}}{N} - {\overline{y}}^{2}}\rbrack \times N$$

Note: The above equations omit weights for the sake of simplicity; H2O-3
includes weights in its calculation of squared error.

**H2O Feature Importance Reference**

Rifkin, Ryan and Klautau, Aldebaro. \"In Defense of One-Vs-All
Classification.\" J. Mach. Learn. Res. (2004):101-141.
(http://www.jmlr.org/papers/v5/rifkin04a.html)
