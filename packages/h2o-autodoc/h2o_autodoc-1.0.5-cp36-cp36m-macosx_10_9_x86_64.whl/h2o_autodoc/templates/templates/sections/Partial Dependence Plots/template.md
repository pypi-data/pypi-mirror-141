{% if pdp._experiment.parameters.is_classification and pdp._experiment.labels | length != 2 %}

Partial dependence plots are currently not supported for multiclass classification.

{% else %}

Partial dependence plots show the partial dependence as a function of specific values for a feature subset. The plots show how machine-learned response functions change based on the values of an input feature of interest, while taking nonlinearity into consideration and averaging out the effects of all other input features. Partial dependence plots enable increased transparency in a model and enable the ability to validate and debug a model by comparing a feature's average predictions across its domain to known standards and reasonable expectations. 

{% set pdp_plots = pdp. get_dai_pdp_ice_plots (config.autodoc_num_features) %}

The partial dependence plots are shown for the top {{pdp_plots| length | int }} original variables. The top {{pdp_plots| length | int}} original variables are chosen based on their Component Based Variable Importance.{% if pdp._max_runtime_seconds == 0 %}Partial Dependence computation reached maximum allowed time {{pdp._timeout}} seconds.{% endif %}

{% if user_defined_individuals and pdp_plots| length > 0 and pdp._individual_rows %}

ICE records are included on the Partial Dependence Plot. Records were manually selected and are labeled in the legend with the form "ICE row {row index}."{% elif  not user_defined_individuals and pdp_plots| length > 0%}

ICE records were automatically selected and are labeled in the legend with the form "ICE row {row index}." By default, the records are binned into quantiles and the first record from each bin is selected.

{% else %}

{% endif %}

{% if pdp_plots| length > 0 %}

**Plot Details**

In the Driverless AI PDP, the y-axis represents the mean response, and a shaded region (for numeric features) or shaded bar (for categorical features) represents ± 1 standard deviation. Out-of-range PDP (diamond markers) represent values outside feature intervals seen in the data, unseen categorical values, or missing values.

For continuous features, numeric values up to {{ config.autodoc_out_of_range }}  standard deviations lower than the minimum training value and higher than the maximum training value are feed into the model. For categorical features, an unseen categorical value is feed into the model denoted by UNSEEN (if the categorical value "UNSEEN" already exists in the training data, the out-of-range is done on a value called "UNSEEN_[x]," where x is some integer). 

{% endif %}

{% for feature, info in pdp_plots.items() %}

Feature **{{ info["display_text"] }}**

{{ info["rendered_image"]}}

{% endfor %}

{% endif %}

