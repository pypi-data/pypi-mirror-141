### Assumptions and Limitations

Driverless AI trains all models based on the training data provided (in this case: *{{experiment.parameters.dataset.display_name|e}}*). It is the assumption of Driverless AI that this dataset is representative of the data that will be seen when scoring.

Driverless AI may perform shift detection between the {{data_info._comparison_string}}.  If a shift in distribution is detected, this may indicate that the data that will be used for scoring may have distributions not represented in the training data.  {% if valid_predictions_path == '' %} The model may have poorer performance than seen on the internal validation data. {% endif %}

For this experiment, Driverless AI {% if experiment.test_predictions_path == '' and experiment.valid_predictions_path == ''%} was not able to detect any shift in distribution between {{data_info._comparison_string}} because no validation or test data was provided. {% elif experiment_overview._internal_args.check_distribution_shift == False %} did not detect any shift in distribution because shift detection was turned off due to the accuracy setting (increase accuracy setting for shift detection). {% elif data_info._shift_table == None %} performed shift detection but found no significant changes in the distribution of the {{data_info._comparison_string}}. {% else %} performed shift detection and found significant differences described below: 

{{data_info._shift_table}}

{% endif %}

