### Training Data
The training data consists of {% if data_info._train_summary.numeric_summary|length > 0 and data_info._train_summary.categorical_summary|length> 0 %} both numeric and categorical columns.  {% elif data_info._train_summary.categorical_summary|length == 0 %} only numeric columns. {% else %} only categorical columns. {% endif %}

The summary of the columns is shown below{% if config.autodoc_data_summary_col_num < data_info.train_ncols and config.autodoc_data_summary_col_num > 0  %}(limited to the top {{ config.autodoc_data_summary_col_num }} features){%endif%}:

{% if data_info._train_summary.numeric_summary|length > 0 %}

#### Numeric Columns

{{data_info._train_summary.numeric_summary}}

{% endif %} 

{% if data_info._train_summary.boolean_summary|length > 0 %}

#### Boolean Columns

{{data_info._train_summary.boolean_summary}}

{% endif %} 

{% if data_info._train_summary.categorical_summary|length > 0 %}

#### Categorical Columns

{{data_info._train_summary.categorical_summary}}

{% endif %}
	