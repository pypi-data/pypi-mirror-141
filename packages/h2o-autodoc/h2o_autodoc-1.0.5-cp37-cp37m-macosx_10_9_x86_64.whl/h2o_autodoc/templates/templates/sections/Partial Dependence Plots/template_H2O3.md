{% if pdp == None %}

Partial dependence plots are currently not supported for multiclass classification.{% else %}Partial dependence plots show the partial dependence as a function of specific values for a feature subset. The plots show how machine-learned response functions change based on the values of an input feature of interest, while taking nonlinearity into consideration and averaging out the effects of all other input features. Partial dependence plots enable increased transparency in a model and enable the ability to validate and debug a model by comparing a feature's average predictions across its domain to known standards and reasonable expectations.

{% set pdp_plots = pdp. get_dai_pdp_ice_plots (top_n=config.plot_num_features, include_histograms=config.include_hist) %}{% if pdp_plots == [] %}Partial dependence plots are not shown because they were disabled in the report configurations. {% else %}The partial dependence plots are shown for {% if pdp.pdp_selection == "top" %}the top {{pdp_plots| length | int }} original variables. The top {{pdp_plots| length | int}} original variables are chosen based on their model specific variable importance.{% elif  pdp.pdp_selection == "user"%}{{pdp_plots| length | int }} user-selected features.{% elif  pdp.pdp_selection == "all"%}all {{pdp_plots| length | int }} features.{% else %}{{pdp_plots| length | int }}original variables.{% endif %}{% endif %}

{% if pdp_plots| length > 0 %}

**Plot Details**

In the {{ package_name }} PDP, the y-axis represents the mean response, and a shaded region (for numeric features) or shaded bar (for categorical features) represents ± 1 standard deviation.

{% for feature, info in pdp_plots.items()%}

Feature **{{feature|e}}**{{ info ["rendered_image"]|e}}

{% endfor %}{% endif %}{% endif %}
