{% if experiment.test_predictions_path != '' %}

#### Test Data

The test data consists of {% if data_info._test_summary.numeric_summary|length > 0 and  data_info._test_summary.categorical_summary|length> 0 %} both numeric and categorical columns.  {% elif data_info._test_summary.categorical_summary|length == 0 %} only numeric columns.{% else %} only categorical columns.

{% endif %} 

The descriptive summary for each column is shown below:

{% if data_info._test_summary.numeric_summary|length > 0 %}

**Numeric Columns**

{{data_info._test_summary.numeric_summary}}


{% endif %} 

{% if data_info._test_summary.boolean_summary|length > 0 %}

**Boolean Columns**

{{data_info._test_summary.boolean_summary}}

{% endif %}

{% if data_info._test_summary.categorical_summary|length > 0 %}

**Categorical Columns**

{{data_info._test_summary.categorical_summary}}

{% endif %}

**Unseen Levels in the Test Set**

{% if data_info.get_unseen_test_categoricals() %}

{{package_name}} detected unseen levels in the test dataset. The frequency count for the top 20 unseen levels of each features is shown below. 

{% for feature, table in data_info.get_unseen_test_categoricals(20).items() %}

**Feature {{feature}}**

{{table}}

{% endfor %}

{% else %}

The test dataset does not contain any categorical levels that were not seen in the training dataset.

{% endif %}

{% if data_info._test_missing_df != None %} 

**Missing Values**

{% if (data_info._test_missing_df != 0) and (data_info._test_missing_df is not string) %} 

Features with missing values and their missing-value total count are shown in the table below:

{{data_info._test_missing_df}}

{% elif data_info._test_missing_df == 0 %}

{{package_name}} did not find any missing values in the test dataset.

{% else %} 

{% endif %} 

{% endif %}

{% endif %}

{{package_name}}