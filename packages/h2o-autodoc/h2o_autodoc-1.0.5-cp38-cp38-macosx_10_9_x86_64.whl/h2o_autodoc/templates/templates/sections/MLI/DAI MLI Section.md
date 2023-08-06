{% if mli %}

{% if placeholders.keys() | length > 0 %}

{% for title, info in placeholders.items()%}

{% if 'code{{' in title %}

***{{title}}***

{{info }}

{% else %}

***{{title}}***

{{info }}

{% endif %}

{% endfor %}

{% endif %}
{% if mli.has_klime() %}

{{ section.render('MLI.KLIME Global Top Bottom Coefs and Clusters')
}}

*Surrogate GLM Predictions*

{{ section.render('MLI.KLIME Plot')}}
{% endif %}{%if mli.has_dt() %}

**Decision Tree Surrogate Plot**

{{ section.render('MLI.Surrogate DT')}}
{% endif %}

#### Local Interpretation

This section aims to provide a local understanding of the final model's
decisions. The interpretation is given at a record level. The local
interpretation techniques available are described as follows:

{{ section.render('MLI.KLIME Reason Code Text')}}

**Leave-One-Covariate-Out (LOCO)**

Leave-one-covariate-out (LOCO) provides a mechanism for calculating
feature importance values for any model on a per-observation basis by
subtracting the model's prediction for an observation of data from the
model's prediction for that observation of data without an input
feature of interest. In the Driverless AI LOCO plot, local feature
importance values are displayed under global feature importance values
for each feature.

**Individual Conditional Expectation Plots**

Partial dependence plots show the partial dependence as a function of
specific values for a feature subset. The plots show how machine-learned
response functions change based on the values of an input feature of
interest, while taking nonlinearity into consideration and averaging out
the effects of all other input features.

Individual conditional expectation (ICE) plots, a newer and less
well-known adaptation of partial dependence plots, can be used to create
more localized explanations for a single observation of data using the
same basic ideas as partial dependence plots. ICE is also a type of
nonlinear sensitivity analysis in which the model predictions for a
single observation are measured while a feature of interest is varied
over its domain.

ICE plots enable a model developer to answer questions about the
Driverless AI model's prediction for an individual observation of data,
such as:

-   Is it outside one standard deviation from the average model behavior
    represented by partial dependence?

-   Is the treatment of a specific observation valid in comparison to
    average model behavior, known standards, domain knowledge, and
    reasonable expectations?

-   How will the observation behave in hypothetical situations where one
    feature, in a selected observation is varied across its domain?

For each of the records selected by the user, the following
interpretability tools are displayed:

-   The record's original feature values

-   The record's K-LIME reason codes

-   A Leave-One-Covariate-Out (LOCO) Plot

-   For the top features, a plot with Individual Conditional Expectation
    (ICE) curves overlaying the PDP is shown

{{ section.render('MLI.Local Interpretability Row Information',
show_row_value=True, show_klime_table=True, show_loco_plot=True,
show_ice_plots=True)}}

{% else %}

Driverless AI was not able to calculate: Surrogate Models, Partial
Dependence Plots, Leave One Covariate Out (LOCO), *K*-LIME Reason Codes,
or Individual Conditional Expectation Plots (ICE) because {% if
experiment_overview._problem_type == "multinomial" %}this is not
supported for multinomial experiments.{% elif
experiment.parameters.is_timeseries == True %}this is not supported for
time series experiments. {% else %} Model Interpretability was not run.
{% endif %}{% endif %}
