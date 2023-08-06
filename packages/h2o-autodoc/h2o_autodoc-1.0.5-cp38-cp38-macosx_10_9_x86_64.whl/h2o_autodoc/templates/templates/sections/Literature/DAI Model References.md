**RuleFit** is an algorithm that incorporates interaction terms into a Generalized Linear Model. RuleFit does this by including rule-based Boolean features that were extracted from tree-based models. 

Reference: Friedman, Jerome H., and Bogdan E. Popescu. "Predictive learning via rule ensembles." The Annals of Applied Statistics2.3 (2008): 916-954.

**XGBoost** is a supervised learning algorithm that implements a process called boosting to yield accurate models. Boosting refers to the ensemble learning technique of building many models sequentially, with each new model attempting to correct for the deficiencies in the previous model. In tree boosting, each new model that is added to the ensemble is a decision tree. To enhance machine learning speed and performance, the XGBoost package implements novel techniques for boosting trees in parallel.

Reference: Chen, Tianqi, and Carlos Guestrin. "Xgboost: A scalable tree boosting system." Proceedings of the 22nd ACM SIGKDD international conference on knowledge discovery and data mining. ACM, 2016.

Software Citation: https://github.com/dmlc/xgboost

**XGBoost DART** is a supervised learning algorithm that implements a process called boosting to yield accurate models. Boosting refers to the ensemble learning technique of building many models sequentially, with each new model attempting to correct for the deficiencies in the previous model. In tree boosting, each new model that is added to the ensemble is a decision tree. XGBoost DART was introduced to prevent XGBoost GBM’s “over-specialization,” where newly added trees only focus on correcting a few observations that may not improve the overall ensemble’s performance. Instead of fitting a new tree with respect to all previous trees, DART selects one with respect to a random subset of the previous trees. A scaling factor is then applied to the new tree, to account for the dropped trees. To enhance machine learning speed and performance, the XGBoost package implements novel techniques for boosting trees in parallel. The step to randomly select a subset of trees, however, can cause XGBoost DART to be slower than XGBoost GBM, because it requires the gradients and residuals to be recalculated.

Reference: K. V. Rashmi and Ran Gilad-Bachrach. "DART: Dropouts meet Multiple Additive Regression Trees." Proceedings of the 18th International Conference on Artificial Intelligence and Statistics (AISTATS) 2015, San Diego, CA, USA. JMLR: W&CP volume 38.

Software Citation: https://github.com/dmlc/xgboost

**GLM** (an XGBoost model with a linear booster): Generalized Linear Models (GLM) are an extension of traditional linear models and have the ability to estimate regression models for outcomes following exponential distributions. In addition to the Gaussian (i.e. normal) distribution, these include Poisson, binomial, and gamma distributions. Each serves a different purpose, and depending on the distribution and link function choice, can be used either for regression or classification.

Reference: Hastie, Trevor, Tibshirani, Robert, and Friedman, Jerome. The Elements of Statistical Learning. Springer, 2008.

**LightGBM** is an implementation of Gradient Boosting Machines designed to enhance computational speed while training a model. It does this by using two new techniques: Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB). The first technique is designed to reduce the number of observations the algorithm needs to scan to find the best split point. The second technique reduces the number of features the algorithm scans, to help prevent slowdowns for high dimensional datasets. 

Reference: Ke, Guolin, et al. "Lightgbm: A highly efficient gradient boosting decision tree." Advances in Neural Information Processing Systems. 2017.)

Software Citation: https://github.com/Microsoft/LightGBM

**TensorFlow** is a computational framework for machine learning that implements several different machine learning algorithms. Currently, Driverless AI implements TensorFlow’s Multi-Layer Perceptron, and Convolutional Neural Nets for its NLP recipes. 

Reference: Abadi, Martín, et al. "Tensorflow: a system for large-scale machine learning." OSDI. Vol. 16. 2016.)

**FTRL** Follow the Regularized Leader (FTRL) is a DataTable implementation of the FTRL-Proximal online learning algorithm proposed in McMahan, H. Brendan, et al. This implementation uses a hashing trick and Hogwild approach for parallelization. FTRL supports binomial and multinomial classification for categorical targets, as well as regression for continuous targets.

Software Citation for DataTable: https://github.com/h2oai/datatable

Reference FTRL Algorithm: McMahan, H. Brendan, et al. “Ad click prediction: a view from the trenches.” Proceedings of the 19th ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2013.

Reference Hogwild Algorithm: Niu, Feng, et al. “Hogwild: A lock-free approach to parallelizing stochastic gradient descent.” Advances in neural information processing systems. 2011.

