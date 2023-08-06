{% if psi and (psi._test_preds.keys() | length > 0) %}

**Population Stability Index (PSI) Final Model Details**

Population Stability Index is a statistic used to describe a variable's distribution shift. It can measure the shift between the training dataset's model score distribution and any other given dataset (i.e. validation or test dataset). 

A PSI value lower than 0.10 indicates a small shift in the model predictions, a value between 0.10 and 0.25 indicates a moderate shift, and a value greater than 0.25 indicates a strong shift. Strong shift values can indicate that the model trained on the training dataset might not be suitable for the provided validation or test datasets.

The PSI and calculation table is provided for each dataset below. The corresponding table columns are defined as follows:

- *Quantile: the bin to which the ordered predicted probabilities belong.*

- *Upper Bound: the upper bound of the corresponding bin.*

- *Test Count: the total number of Test records within the corresponding bin.*

- *Test Fraction (Tst): Test Count divided by the total number of Test records.*

- *Train Count: the total number of Train records within the corresponding bin.*

- *Train Fraction (Trn): Train Count divided by the total number of Train records.*

- *Tst - Trn: the difference between the Test Fraction and the Train Fraction.*

- *ln(Tst / Trn): the natural logarithm of the Test Fraction divided by the Train Fraction.*

- *PSI: the Population Stability Index for each bin - the dataset PSI is the total sum of these PSI values.*

{% set psi_results = psi.get_psi(config.autodoc_population_stability_index_n_quantiles) %}{% for split, psi_result in psi_results["psi"].items() %}

**{{split}}**

The Population Stability Index is {{ '{0:.4}'.format(psi_result["score"]) }}.

{{psi_result["table"]}}

{% endfor %}
{% endif %}