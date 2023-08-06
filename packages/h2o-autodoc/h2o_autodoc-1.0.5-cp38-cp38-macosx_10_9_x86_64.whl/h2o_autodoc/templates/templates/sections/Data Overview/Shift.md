#### Shifts Detected

{{ package_name }}  can perform shift detection between the training, validation, and testing datasets. It does this by training a binomial model to predict which dataset a record belongs to. For example, it may find that it is able to separate the training and testing data with an AUC of 0.8 using only the column: C1 as the predictor. This indicates that there is some sort of drift in the distribution of C1 between the training and testing data.

{% if experiment.test_predictions_path == '' and experiment.valid_predictions_path == '' %}For this experiment, {{ package_name }}  was not able to check for distribution shifts because only the training dataset was supplied by the user. {% elif experiment_overview._internal_args.check_distribution_shift == False %}For this experiment, {{ package_name }}  was not able to check for distribution shifts between the {{data_info._comparison_string}} because the accuracy setting was too low. To turn on shift detection, increase the accuracy setting. {% elif data_info._shift_table == None %}For this experiment, {{ package_name }}  checked the {{data_info._comparison_string}} for any shift in distributions but found none.  This indicates that all the predictors/columns in the {{data_info._comparison_string}} are from the same distribution. {% else %}For this experiment, {{ package_name }}  checked the {{data_info._comparison_string}} for any shift in distribution and found the following significant differences:

{% for shift in data_info._shift_info %}

- {{shift.shift_warning|e}} {% if shift.data_type == "int" or shift.data_type == "real" %}

{{ images.get(shift.filename)}} 

{% endif %}{% endfor %}{% endif %}