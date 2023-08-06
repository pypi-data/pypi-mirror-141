{% if response_rates %}

**Quantile Response Rates**

The response rate, for a given quantile, is equal to the number of positive-labeled data points divided by the total number of data points. Quantiles are sorted in decreasing order.

{% set responses = response_rates. get_response_rates (config.autodoc_response_rate_n_quantiles)%}

{{ responses ["response_rate_plot"] }} 

**Actual vs Predicted Probabilities**

This plot shows the alignment between the predicted and the actual probabilities. The predicted probabilities are binned into quantiles. For each, bin the average predicted value and the actual response rate (i.e., the number positive-labeled records divided by the total number of records within each bin) is calculated.

{{ responses ["act_vs_pred_prob"] }} 

**Actual vs Predicted Log Odds**

This plot shows the alignment between the predicted and the actual probabilities within the log odds space. In this case, the log odds are the log transformation of the probability of a positive record divided by the probability of a negative record.

{{ responses ["act_vs_pred_odds"] }} 

Details on the quantile-based plots' calculations can be found in the Appendix.
{% endif %}
