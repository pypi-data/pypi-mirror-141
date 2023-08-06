{% if params._params.time_col != '[OFF]' %}Driverless AI automatically split the data into training and validation data, ordering the data by {{params._params.time_col|e}}.{% if params._config.time_series_recipe == True %} The model was tuned to predict {{params._params.num_prediction_periods}} {% if params._params.num_prediction_periods > 1 %}{{params._params.time_unit|e}}s{% else %}{{params._params.time_unit|e}} {% endif %}{% if params._params.num_gap_periods == 0 %} with no gap between training and forecasting.{% else %} with a {{params._params.num_gap_periods}} {{params._params.time_unit|e}} gap between training and forecasting.{% endif %}{% endif %}
{{ validation_schema.time_series_validation_split()}}
{{ validation_schema.time_series_final_back_testing_split()}}
{{ validation_schema.time_series_final_train_split()}}
{% endif %}
