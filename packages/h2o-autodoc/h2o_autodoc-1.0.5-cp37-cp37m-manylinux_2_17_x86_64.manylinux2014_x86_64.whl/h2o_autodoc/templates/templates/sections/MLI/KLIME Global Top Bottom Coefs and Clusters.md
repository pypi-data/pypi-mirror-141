{% if mli and mli.has_klime() %}**K local interpretable model-agnostic (K-LIME)**

K-LIME is a variant of the LIME technique proposed by Ribeiro at al
(2016). K-LIME generates global and local explanations that increase
the transparency of the Driverless AI model. K-LIME creates one global
surrogate GLM on the entire training data. K-LIME also creates
numerous local surrogate GLMs on samples formed from k-means cluster in
the training data.

All GLM surrogates are trained to model the predictions of the
Driverless AI model using the original training data. The number of
clusters for local explanations is chosen by a grid search in which the
R2 between the Driverless AI model predictions and all the local K-LIME
model predictions is maximized.

The parameters of the global K-LIME model give an indication of overall linear feature importance and the overall average direction in which an input variable influences the Driverless AI model predictions. The global model is also used to generate explanations for very small clusters (*N*<20) where fitting a local linear model is inappropriate. The tables show the top positive and negative coefficients based on the global GLM model.

The tables show the top positive and negative coefficients based on the
global GLM model.

{% set global_coefs = mli.top_reason_codes(10, 2)%}

*The Top Positive Global Coefficients*

{{ global_coefs[0] }}

*The Top Negative Global Coefficients*

{{ global_coefs[1]}}

*Cluster Descriptions*

For the local surrogate GLMs, K-means was used to cluster data based on
the top {{ mli.cluster_descriptions()[1] | length }} variables: {{
mli.cluster_descriptions()[1] }}. The clusters used to train each
local surrogate GLM is described below:

{{ mli.cluster_descriptions()[0] }}
{% endif %}