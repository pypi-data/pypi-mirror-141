Driverless AI requires target labels to assess the performance of any dataset. If the model developer has labeled out-of-sample data that was not used for training, they can use Driverless AI to score that dataset and generate additional performance metrics and diagnostics for model discrimination.

{% set pdp_plots = pdp.get_dai_pdp_out_of_range_plots(config. autodoc_num_features) %}

{% if  experiment_overview._problem_type == "multinomial" %}

Driverless AI did not perform Out-of-range PDP, because Driverless AI's Machine Learning Interpretability does not currently support out-of-range PDP for multinomial problems.

{% elif  experiment.parameters.is_timeseries == True %}

Driverless AI did not perform Out-of-range PDP, because Driverless AI's Machine Learning Interpretability does not currently support out-of-range PDP for time series problems.

{% elif pdp_plots| length > 0 %}The following plot shows PDP for out-of-range data:

{% for feature, info in pdp_plots.items() %}

Feature ***{{feature}}***

{{ info ["rendered_image"]}}

{% endfor %}

{% else %}

Driverless AI did not perform Out-of-range PDP. The partial dependence plots are not shown for text features.

{% endif %}{% if pdp._max_runtime_seconds == 0 %} Partial Dependence computation reached maximum allowed time {{pdp._timeout}} seconds.{% endif %}

