**Parameters Considered**

{% if model_tuning._tuning_tables | length == 1  %}

The table below shows a portion of the different parameter configurations evaluated by Driverless AI for the {{model_tuning._tuning_algos}} and their score and training time.  The table is ordered based on a combination of {{scorer_direction}} score and lowest training time.

{% for key, value in model_tuning._tuning_tables.items()%}

{{value}}

{% endfor %} {% else %}

The table below shows the score and training time of the {{model_tuning._tuning_algos}} evaluated by Driverless AI.  The table shows the {% if model_tuning._num_tuning_models > 10 %} top 10 {% endif %}parameter tuning models evaluated, ordered based on a combination of {{scorer_direction}} score and lowest training time.

{{model_tuning._tuning_tables.get("combo")}}

{% endif %}
