{% if mli and experiment_overview._problem_type != "multinomial" %}

K-LIME is a variant of the LIME technique proposed by Ribeiro et al. (2016). K-LIME generates global and local explanations that increase the transparency of the Driverless AI model. K-LIME creates one global surrogate GLM on the entire training data. K-LIME also creates numerous local surrogate GLMs on samples formed from K-means clusters in the training data. This section focuses on the global surrogate GLM. 

Since the global GLM model is a linear model, reason code values are calculated by determining each coefficient-feature product. Whether the task is classification or regression, positive reason codes increase the output of the K-LIME model and negative reason code values decrease the output of the K-LIME model. 

Note: Categorical features of the form *FeatureName.FeatureLevel* represent features that have been one-hot-encoded. {% if config.autodoc_global_klime_num_tables < 2  %}

The following table shows the top coefficients based on the global K-LIME GLM model.

{{mli.top_reason_codes(config.autodoc_global_klime_num_features, config.autodoc_global_klime_num_tables)}}

{% else %}

The following tables show the top positive and negative coefficients based on the global K-LIME GLM model.

The Top Positive K-LIME Global GLM Coefficients

{{mli.top_reason_codes(config.autodoc_global_klime_num_features, config.autodoc_global_klime_num_tables)[0]}}

The Top Negative K-LIME Global GLM Coefficients

{{mli.top_reason_codes(config.autodoc_global_klime_num_features, config.autodoc_global_klime_num_tables)[1]}}

{% endif %}

{% endif %}

