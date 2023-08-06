**K local interpretable model-agnostic (K-LIME) Reason Codes**

K-LIME reason code values provide a model developer with a feature's
approximate local, linear contribution to the Driverless AI final model.
Reason codes are powerful tools for accountability and fairness because
they provide an explanation for each prediction, enabling a model
developer to understand the approximate magnitude and direction of an
input feature's local contribution for the Driverless AI final model.

K-LIME can create these reason codes through the surrogate GLM models it
creates. K-LIME trains one global surrogate GLM on the entire training
data as well as numerous local surrogate GLMs on samples formed from
k-means cluster in the training data. If the local surrogate GLM has a
lower R2 value than the global surrogate GLM, the global surrogate GLM
is used for the records in that cluster.

Since the surrogate GLMs are linear models, reason code values are
calculated by determining each coefficient-feature product.
