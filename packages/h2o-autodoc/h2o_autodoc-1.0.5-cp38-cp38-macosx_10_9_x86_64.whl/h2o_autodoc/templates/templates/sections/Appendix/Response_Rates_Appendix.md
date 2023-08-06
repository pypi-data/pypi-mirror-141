{% if response_rates %}

**Quantile Plots Calculation Table**

The following table is used to calculate the Quantile Response Rates, Actual vs Predicted Probabilities, and Actual vs Predicted Log Odds plot.
table columns are defined as follows:

- *Quantile: the bin to which the ordered predicted probabilities belong.*

- *bound: the upper bound of the corresponding bin.*

- *{dataset name} cnt: the number of records within the corresponding bin.*

- *{dataset name} sum: the number of positive-labeled records within the corresponding bin.* 

- *{dataset name} act: the fraction of positive-labeled records within the corresponding bin.*

- *{dataset name} pred: the mean of the predicted values that fall within the corresponding bin.*

{% set responses = response_rates. get_response_rates (config.autodoc_response_rate_n_quantiles)%}

{{responses["table"]}}

{% endif %}