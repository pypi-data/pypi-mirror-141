**Missing Values Handling**

How Driverless AI handles the input datasets depends on the final model. For the *{{ experiment.description}}* experiment, Driverless AI built {% if final_model._num_ensemble_models > 0 %} a Stacked Ensemble ({{final_model._final_model_string}}).

{% else %}

{{final_model._final_model_string}}.

{% endif %} The following section describes the relevant handling of missing values. 

#### Missing Values During Training

{% if ('XGBoostGBMModel' in final_model._final_model_string) or ('LightGBMModel' in final_model._final_model_string) or ('RuleFitModel' in final_model._final_model_string) %}

Driverless AI treats missing values natively (i.e., a missing value is treated as a special value). Experiments rarely benefit from imputation techniques, unless the user has a strong understanding of the data.

{% endif %}

{% if final_model._glm_in_final %}

Driverless AI automatically performs mean value imputation (equivalent to setting the value to zero after standardization).

{% endif %}

{% if ('TensorFlowModel' in final_model._final_model_string) %}

Driverless AI provides an imputation setting for TensorFlow in the config.toml file: tf_nan_impute_value (post-normalization). If you set this option to 0, then missing values will be imputed by the mean. Setting it to (for example) +5 will specify 5 standard deviations above the mean of the distribution. The default value in Driverless AI is -5, which specifies that TensorFlow will treat missing values as outliers on the negative end of the spectrum. Specify 0 if you prefer mean imputation.

{% endif %}

{% if ('FTRLModel' in final_model._final_model_string) %}

In FTRL, missing values have their own representation for each datable column type. These representations are used to hash the missing value, with their column’s name, to an integer. This means FTRL replaces missing values with special constants that are the same for each column type, and then treats these special constants like a normal data value.

{% endif %}


#### Missing Values During Scoring (Production)

{% if ('XGBoostGBMModel' in final_model._final_model_string) or ('LightGBMModel' in final_model._final_model_string) or ('RuleFitModel' in final_model._final_model_string) %}

If missing data is present during training, these tree-based algorithms learn the optimal direction for missing data for each split (left or right). This optimal direction is then used for missing values during scoring. If no missing data is present during scoring (for a particular feature), then the majority path is followed if the value is missing.

{% endif %}

{% if final_model._glm_in_final %}

Missing values are replaced by the mean value (from training), same as in training.

{% endif %}

{% if ('TensorFlowModel' in final_model._final_model_string) %}

Missing values are replaced by the same value as specified during training (parameterized by tf_nan_impute_value).

{% endif %}

{% if ('FTRLModel' in final_model._final_model_string) %}

To ensure consistency, FTRL treats missing values during scoring in exactly the same way as during training.

{% endif %}


##### Clustering in Transformers
Missing values are replaced with the mean along each column. This is used only on numeric columns.

##### Isolation Forest Anomaly Score Transformer
Isolation Forest uses out-of-range imputation that fills missing values with the values beyond the maximum.


#### Predict on a Categorical Level Not Seen During Training
{% if ('XGBoostGBMModel' in final_model._final_model_string) or ('LightGBMModel' in final_model._final_model_string) or ('RuleFitModel' in final_model._final_model_string) or ('TensorFlowModel' in final_model._final_model_string) or (final_model._glm_in_final) %}

Driverless AI’s feature engineering pipeline will compute a numeric value for every categorical level present in the data, whether it’s a previously seen value or not. For frequency encoding, unseen levels will be replaced by 0. For target encoding, the global mean of the target value will be used.

{% endif %}

{% if ('FTRLModel' in final_model._final_model_string) %}

FTRL models don’t distinguish between categorical and numeric values. Whether or not FTRL saw a particular value during training, it will hash all the data, row by row, to numeric and then make predictions. Because you can think of FTRL as learning all the possible values in the dataset by heart, there is no guarantee it will make accurate predictions for unseen data. Therefore, it is important to ensure that the training dataset has a reasonable “overlap” in terms of unique values with the ones used to make predictions.

{% endif %}

##### Missing Values in Response
All algorithms will skip an observation (record) if the response value is missing.

