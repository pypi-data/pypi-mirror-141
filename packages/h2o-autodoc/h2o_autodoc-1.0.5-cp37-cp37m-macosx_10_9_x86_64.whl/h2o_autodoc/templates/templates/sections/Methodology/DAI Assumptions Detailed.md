{% if experiment.valid_predictions_path == '' %}

For this experiment, no validation data was provided.  {% if params._params.time_col == '[OFF]' %} Because no validation data was provided, the model was evaluated on randomly sampled data created by Driverless AI. {% else %} Because no validation data was provided, the model was evaluated on a time-based sample created by Driverless AI. {% endif %} If this sample does not mimic the data used during scoring, results may be worse than estimated. {% endif %}

{% if experiment.valid_predictions_path != '' or experiment.test_predictions_path != '' %}

{% if experiment_overview._internal_args.check_distribution_shift == False %}

Driverless AI may perform shift detection between the {{data_info._comparison_string}}.  If a shift in distribution is detected, this may indicate that the data that will be used for scoring may have distributions not represented in the training data.  

For this experiment, Driverless AI was not able to detect any shift in distribution because shift detection was turned off due to the accuracy setting (increase accuracy setting for shift detection).  Because shift detection was turned off, it is possible that there may be shifts occurring in variables that the user was not alerted to. This could lead to poor performance of the model in production because the scoring data may not mimic the data seen during training.

{% endif %} 

{% if data_info._shift_cols | length > 0 %}

Driverless AI may perform shift detection between the {{data_info._comparison_string}}.  If a shift in distribution is detected, this may indicate that the data that will be used for scoring may have distributions not represented in the training data.  

For this experiment, Driverless AI checked the {{data_info._comparison_string}} for any shift in distribution and found the following significant differences:

{% for shift in data_info._shift_strings %}

{{shift}} 

{% endfor %}

The user should consider removing these variables as predictors from the experiment since they may not be reliable. The shift could indicate poor performance of the model in production because the scoring data may not mimic the data seen during training.

{% endif %}

{% endif %}

