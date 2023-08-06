**Final Model Description**

The architecture of the final model is described below:

{{section.render('Final Model.DAI Final Model Components Table')}}

{% if final_model._num_ensemble_models > 0 %}

More detailed parameters of each model in the final stacked ensemble are described below.

{% else %}

More detailed parameters of the final model are described below.

{% endif %} 

{% for key_table, value_table in final_model._final_model_desc.base_learners.items() %}

- {{value_table.string}}

{{value_table.params}}

{% endfor %}

