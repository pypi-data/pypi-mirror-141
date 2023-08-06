{% if model_tuning._perf_tables | length %}The alternative model section consists of two part: alternative model performance and parameters. The performance section shows how each alternative model performed for a given dataset split (train, valid, test, etc.,). Performance tables are sorted by  **{{model_tuning._default_metric.upper()}}**. The parameter section provides the model arguments which a user has the control to grid over. Note: The parameter value "auto" corresponds to the default value for that model's H2O-3 version.  

**PERFORMANCE OVERVIEW TABLE**
{{ model_tuning._alt_overview_perf_tables }}

**PERFORMANCE TABLES**{% for key, value in model_tuning._perf_tables.items()%}

**{{ key.title()|e }}  Data Split**

{{value}}{% endfor %}{% endif %}


{% if model_tuning._tuning_tables | length %}**PARAMETER TUNING TABLES**{% for key, value in model_tuning._tuning_tables.items()%}

**{{ key.title()|e }} Tuning**

{{model_tuning._alt_model_desc(key)}}

{{value}}

{% endfor %}{% else %}Alternative models were not provided by the user.{% endif %}
