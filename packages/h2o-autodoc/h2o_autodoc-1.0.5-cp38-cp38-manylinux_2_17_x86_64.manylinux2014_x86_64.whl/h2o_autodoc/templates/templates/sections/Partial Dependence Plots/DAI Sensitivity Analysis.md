Sensitivity analysis investigates what happens to a model's predictions if the input values are varied. Partial Dependence Plots (PDP) and Individual Conditional Expectation (ICE) are machine learning interpretability techniques that together provide an overview of the model's results when performing sensitivity analysis.
 
Partial dependence plots show the partial dependence as a function of specific values for a feature subset. The plots show how machine-learned response functions change based on the values of an input feature of interest, while taking nonlinearity into consideration and averaging out the effects of all other input features. Partial dependence plots enable increased transparency in a model and enable the ability to validate and debug a model by comparing a feature's average predictions across its domain to known standards and reasonable expectations. In the Driverless AI PDP, the y-axis represents the mean response, and a shaded region (for numeric features) or shaded bar (for categorical features) represents ± 1 standard deviation.

Individual conditional expectation (ICE) plots, a newer and less well-known adaptation of partial dependence plots, can be used to create more localized explanations for a single observation of data using the same basic ideas as partial dependence plots. ICE is also a type of nonlinear sensitivity analysis in which the model predictions for a single observation are measured while a feature of interest is varied over its domain.

ICE plots enable a model developer to assess the Driverless AI model's prediction for an individual observation of data:

- Is it outside one standard deviation from the average model behavior represented by partial dependence?

- Is the treatment of a specific observation valid in comparison to average model behavior, known standards, domain knowledge, and reasonable expectations?

- How will the observation behave in hypothetical situations where one feature, in a selected observation is varied across its domain?

{% set pdp_plots = pdp. get_dai_ice_out_of_range_plots (config.autodoc_num_features) %}

{% if  experiment_overview._problem_type == "multinomial" %}

Driverless AI did not perform PDP or ICE, because Driverless AI's Machine Learning Interpretability does not currently support PDP or ICE for multinomial problems.

{% elif  experiment.parameters.is_timeseries == True %}

Driverless AI did not perform PDP or ICE, because Driverless AI's Machine Learning Interpretability does not currently support PDP or ICE for time series problems.

{% elif pdp_plots| length > 0 %}

{% set individuals=pdp.get_formatted_individuals() %}

Given the previously described interpretability techniques, this section is structured such that for each record (i.e., rows, observations):

- The record's original feature values are listed.

- For each feature of interest, a plot with ICE curves overlaying the PDP is shown. 

{% for row, info in individuals.items()%}

ROW: {{row}}

{{info}}

ICE PLOTS FOR ROW: {{row}}

{% for feature,  ice in pdp_plots[row].items()  %}

{{ice["rendered_image"]}}

{% endfor %}

{% endfor %}

{% else %}

Driverless AI did not perform PDP. The partial dependence plots are not shown for text features.{% endif %}{% if pdp._max_runtime_seconds == 0 %} Partial Dependence computation reached maximum allowed time {{pdp._timeout}} seconds.{% endif %}

