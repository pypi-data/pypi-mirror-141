{% if psi and (psi._test_preds.keys() | length > 0) %}

**Population Stability Index (PSI)**

Population Stability Index is a statistic used to describe a variable's distribution shift. It can measure the shift between the training dataset's model score distribution and any other given dataset (i.e. validation or test dataset). 

A PSI value lower than 0.10 indicates a small shift in the model predictions, a value between 0.10 and 0.25 indicates a moderate shift, and a value greater than 0.25 indicates a strong shift. Strong shift values can indicate that the model trained on the training dataset might not be suitable for the provided validation or test datasets.

{% set psi_results = psi.get_psi(config.autodoc_population_stability_index_n_quantiles) %} 

**Summary PSI table**

{{psi_results["summary"]}}

Details on the PSI calculations can be found in the Appendix.
{% endif %}
