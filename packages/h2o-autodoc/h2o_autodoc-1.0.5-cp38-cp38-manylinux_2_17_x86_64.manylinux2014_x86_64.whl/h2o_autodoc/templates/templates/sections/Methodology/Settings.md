### Experiment Settings

Below are the settings selected for the experiment by {{generated_by|e}}. The Defined Parameters represent the high-level parameters. 

**Defined Parameters**

{{params.get_user_defined_parameters()}}

{% if not final_model._h2o %}

These Accuracy, Time, and Interpretability settings map to the following internal configuration of the Driverless AI experiment: 

{{params.get_internal_parameters_table()}}

#### Details

- **data filtered**: Driverless AI may filter the training data depending on the number of rows and the Accuracy setting.
    - for this experiment,{% if experiment_overview._internal_args.max_rows < train_data.row_count %} the training data was filtered from {{"{:,}".format(train_data.row_count)}} to {{"{:,}".format(experiment_overview._internal_args.max_rows)}} rows. This filtering can be prevented by increasing the Accuracy setting. {% else %} the training data was not filtered. {% endif %} {% if params._params.is_classification == False %}

- **tune target transform**: whether Driverless AI evaluated the model performance if the target was transformed.
    - ex: the model performance may be better by predicting the log of the target column instead of the raw target column {% endif %}

- **number of feature engineering iterations**: the number of iterations performed of feature engineering.

- **number of models evaluated per iteration**: for each feature engineering iteration, Driverless AI trains multiple models. Each model is trained with a different set of predictors or features. The goal of this step is to determine which types of features lead to the {{scorer_direction}} {{experiment.score_f_name|e}}.

- **early stopping rounds**: if Driverless AI does not see any improvement after {{experiment_overview._internal_args.early_stopping_rounds}} iterations of feature engineering, the feature engineering step is automatically stopped.

- **monotonicity constraint**: if enabled, the models will only have monotone relationships between the predictors and target variable.

- **number of model tuning combinations**: the number of model tuning combinations evaluated to determine the optimal model settings for the {{feature_evolution._feature_evolution_algos|e}}.

- **number of base learners in ensemble**: the number of base models used to create the final ensemble.  

- **time column**: the column that provides the time column. If a time column is provided, feature engineering and model validation will respect the causality of time. If the time column is turned off, no time order is used for modeling and data may be shuffled randomly (any potential temporal causality will be ignored). {% if params._params.time_col != '[OFF]' %}

- **time group columns**: the columns that make up the time series groups. 

- **time period**: the periodicity found in the dataset.

- **number of prediction periods**: the number of periods you want to predict in advance.

- **number of gap periods**: the gap between the data available and the forecast period desired.

{% endif %}

{% endif %}

