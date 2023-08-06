#### Training Data

The training data consists of {% if
data_info._train_summary.numeric_summary|length > 0 and
data_info._train_summary.categorical_summary|length> 0 %} both
numeric and categorical columns. {% elif
data_info._train_summary.categorical_summary|length == 0 %} only
numeric columns. {% else %} only categorical columns.{% endif %} The
descriptive summary for each column is shown below: {% if
data_info._train_summary.numeric_summary|length > 0 %}

**Numeric Columns**

{{ data_info._train_summary.numeric_summary }}                                                                                  

{% endif %}{% if data_info._train_summary.boolean_summary|length > 0 %}

**Boolean Columns**

{{ data_info._train_summary.boolean_summary }}                                                                                

{% endif %}{% if data_info._train_summary.categorical_summary|length > 0 %}

**Categorical Columns**

{{  data_info._train_summary.categorical_summary }}                                                                                      

{% endif %}

{% if package_name == 'H2O-3'%}{%else%}**Categorical Handling**{% if final_features.get_transformation_category('Cross Validation Target Encoding|Frequency Encoding|Cross Validation Categorical to Numeric Encoding') != None %}

For the *{{ experiment.description }}* experiment, {{package_name}} applied
the following categorical transformations.

{{ final_features.get_transformation_category('Cross Validation Target Encoding|Frequency Encoding|Cross Validation Categorical to Numeric Encoding') }}  

{% else %} For the *{{ experiment.description }}* experiment, Driverless
AI did not apply any transformations to features of categorical type.{%
endif %}{% endif %}{% if data_info._train_missing_df != None %}

**Missing Values **

{% if (data_info._train_missing_df != 0) and (data_info._train_missing_df is not string) %}Features with missing values and their missing-value total count are shown in the table below:

{{ data_info._train_missing_df }}                                             

{% elif data_info._train_missing_df == 0 %}{{package_name}} did not find any missing values in the training dataset.{% else %}{% endif %}{% endif %}
