**Residual Analysis**

Residual partial dependence plots (PDP) display the absolute mean error of the model if the value in a select column is varied.  For example, to calculate the residual partial dependence plot, we may set the column STATE to "CA" for all records.  The Driverless AI model is used to predict on this modified data and the mean absolute residual is shown in the plot.

{% set pdp_plots = pdp.get_dai_pdp_out_of_range_plots(config. autodoc_num_features) %}

{% if  experiment_overview._problem_type == "multinomial" %}

Driverless AI did not perform residual PDP, because Driverless AI's Machine Learning Interpretability does not currently support residual PDP for multinomial problems.

{% elif  experiment.parameters.is_timeseries == True %}

Driverless AI did not perform residual PDP, because Driverless AI's Machine Learning Interpretability does not currently support residual PDP for time series problems.

{% elif  pdp_plots| length > 0 %}

The plots below are displayed for the top 10 variables in terms of variable importance.

{% for feature, info in pdp.get_dai_pdp_residual_plots(10).items() %}

Feature ***{{feature}}***

{{ info ["rendered_image"]}}

{% endfor %}

{% else %}

Driverless AI did not perform residual PDP. The partial dependence plots are not shown for text features.

{% endif %}{% if pdp._max_runtime_seconds == 0 %} Partial Dependence computation reached maximum allowed time {{pdp._timeout}} seconds.{% endif %}

