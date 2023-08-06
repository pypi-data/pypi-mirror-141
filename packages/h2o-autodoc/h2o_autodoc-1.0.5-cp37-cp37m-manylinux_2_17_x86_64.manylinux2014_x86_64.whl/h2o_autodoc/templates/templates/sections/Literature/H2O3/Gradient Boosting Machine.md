**Generalized Boosting Machines**

The following algorithm description comes directly from the \"Theory and
Framework\" section in H2O.ai\'s Gradient Boosting Machine with H2O
Booklet (Click et al. 9-10):

*Gradient boosting is a machine learning technique that combines two
powerful tools: gradient-based optimization and boosting. Gradient-based
optimization uses gradient computations to minimize a model\'s loss
function in terms of the training data.*

*Boosting additively collects an ensemble of weak models to create a
robust learning system for predictive tasks. The following example
considers gradient boosting in the example of K-class classification;
the model for regression follows a similar logic. The following analysis
follows from the discussion in Hastie et al (2010) at
http://statweb.stanford.edu/˜tibs/ElemStatLearn/.*

1.  *Initialize* $f_{k0} = 0,k = 1,2,\ldots,K$

2.  *For m = 1 to M:*

<!-- -->

a.  *Set*
    $p_{k}(x) = \frac{e^{f_{k}(x)}}{\sum_{l = 1}^{K}e^{f_{l}(x)}},k = 1,2,\ldots,K$

b.  *For k = 1 to K*

<!-- -->

1.  *Compute*
    $r_{\text{ikm}} = y_{\text{ik}} - p_{k}(x_{i}),i = 1,2,\ldots,N$

2.  *Fit a regression tree the targets*
    $r_{\text{ikm}},i = 1,2,\ldots,N$ *giving terminal regions*
    $R_{\text{jim}},j = 1,2,\ldots,J_{m}$

3.  *Compute*
    $\gamma_{\text{jkm}} = \frac{K - 1}{K}\frac{\sum_{x_{i} \in R_{\text{jkm}}}^{}{(r_{\text{ikm}})}}{\sum_{x_{i} \in R_{\text{jkm}}}^{}|r_{\text{ikm}}|(1 - |r_{\text{ikm}})},j = 1,2,\ldots,J_{m}$

4.  *Update*
    $f_{\text{km}}(x) = f_{k,m - 1}(x) + \sum_{j = 1}^{J_{m}}{\gamma_{\text{jkm}}I(x \in R_{\text{jkm}})}$

<!-- -->

3.  *Output*
    $\overset{\hat{}}{f_{k}}(x) = f_{\text{kM}}(x),k = 1,2,\ldots,K$

*In the above algorithm for multi-class classification, H2O builds
k-regression trees: one tree represents each target class. The index, m,
tracks the number of weak learners added to the current ensemble. Within
this outer loop, there is an inner loop across each of the K classes.*

*Within this inner loop, the first step is to compute the residuals,
r~ikm~, which are the gradient values, for each of the N bins in the
CART model. A regression tree is then fit to these gradient
computations. This fitting process is distributed and parallelized.
Details on this framework are available at
https://www.h2o.ai/blog/building-distributed-gbm-h2o/.*

*The final procedure in the inner loop is to add the current model to
the fitted regression tree to improve the accuracy of the model during
the inherent gradient descent step. After M iterations, the final
\"boosted\" model can be tested out on new data.*
