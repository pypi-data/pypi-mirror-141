{% if model_tuning._tuning_tables | length == 1 %}

The table below shows a portion of the different parameter configurations evaluated by Driverless AI for the {{model_tuning._tuning_algos}} and their score and training time.  The table is ordered based on a combination of {{scorer_direction}} score and lowest training time. 

{% for key_table, value_table in model_tuning._tuning_tables.items()%}

{{value_table}}

{% endfor %}

{% else %}

The table below shows the score and training time of the {{model_tuning._tuning_algos}} evaluated by Driverless AI.  The table is ordered based on a combination of {{scorer_direction}}  {{ experiment.score_f_name }} and lowest training time.

{{model_tuning._tuning_tables.combo}}

More detailed information on the parameters evaluated for each algorithm is shown below.

{% for key, value in model_tuning._tuning_tables.items() if key != "combo" %}

***{{key}} tuning***

*Parameters Optimized*

{{alternative_models._algo_details.arguments.get(key)}}

*Grid Search Results*

{{value}}

{% endfor %}

{% endif %}

