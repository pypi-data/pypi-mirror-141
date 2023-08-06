{% if pred_stats %}

**Prediction statistics**

The following tables and plots show the min, max, mean, and median quantile prediction values for each dataset split. Note: values are rounded to the fourth decimal place. For example, .000025 and .000010 would both appear as 0.0. 

{% for split, prediction_stats in pred_stats. get_prediction_stats (config.autodoc_prediction_stats_n_quantiles).items() %}

**{{split}}**

{{prediction_stats["table"]}}
 
{{prediction_stats["plot"]}} 

{% endfor %}

{% endif %}
