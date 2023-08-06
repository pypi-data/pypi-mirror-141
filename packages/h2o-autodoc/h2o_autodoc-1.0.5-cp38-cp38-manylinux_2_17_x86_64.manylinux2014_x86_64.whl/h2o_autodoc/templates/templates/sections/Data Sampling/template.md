In Driverless AI, data sampling is a pre-processing step that is done before model training begins; it is not related to sampling done during model training. Driverless AI does not perform data sampling unless the dataset is big or highly imbalanced. Whether a dataset is considered big depends on the experiment's accuracy setting and the statistical\_threshold\_data\_size\_large config.toml parameter.

{% if data_info._sampling_desc.downsampled %}Driverless AI sampled down the data because of the *statistical\_threshold\_data\_size\_large* setting and accuracy setting. The data was filtered from {{"{:,}".format(train_data.row_count)}} to {{"{:,}".format(data_info._sampling_desc.sampled_size)}} rows.{% if  data_info._sampling_desc.imbalanced %} Driverless AI performed imbalanced data sampling because the majority class of the target variable occurs more than {{config.imbalance_ratio_sampling_threshold}} times as often as the minority class. The majority class occurs {{"{:,}".format( data_info._sampling_desc.majority_count)}} times in the training data and the minority class only occurs {{"{:,}".format( data_info._sampling_desc.minority_count)}} times. To balance the target class distribution, Driverless AI performed {{data_info._sampling_desc.sampling_type}}.{% else %} Driverless AI used {{data_info._sampling_desc.sampling_type}} to reduce the size of the training data.{% endif %}{% else %}Driverless AI did not perform any down sampling of the data.{% endif %}

{% if final_model.imbalanced_model %}{% set imb_dict = final_model.imbalanced_model %}**Imbalance Model Sampling Techniques**

Only certain DAI models, such as ImbalancedLightGBMModel and ImbalancedXGBoostGBMModel, are designed to handle imbalance data. This category of algorithm can improve performance for binary classification problems with a highly imbalanced target.

**Method Details**

The Imbalance DAI algorithms, train multiple models of the same class on different stratified samples (i.e., bagging) and then combine each model's predictions.
For this experiment, DAI trained {% if final_model._final_model_type == "stacked ensemble" %}a stacked ensemble of {{final_model._final_model_string}}{% elif final_model._final_model_type == "pasting ensemble" %}a bagged ensemble (pasting) of {{final_model._final_model_string}} across {{final_model._num_folds}} folds{% else %}{{final_model._final_model_string}}{% endif %}:{% for key in imb_dict.keys() %}

* {{ key }} trained **{{ imb_dict[key].get('num_bags') }}** internally balanced bagged models. The original target majority to minority count is {{ imb_dict[key].get('original_majority_minority_counts')  }}. The sampled bag target majority to minority counts are: {% for count in imb_dict[key].get('sampled_bag_majority_minority_counts') %}

* {{count}}{% endfor %}

    {{ imb_dict[key].get('config table') }}
    {% endfor %}
{% endif %}