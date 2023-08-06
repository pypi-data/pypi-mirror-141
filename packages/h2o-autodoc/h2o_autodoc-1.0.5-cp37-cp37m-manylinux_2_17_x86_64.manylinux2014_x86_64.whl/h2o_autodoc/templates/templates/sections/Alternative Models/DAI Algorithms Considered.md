**Algorithms Considered**

Driverless AI can evaluate an array of algorithms, including but not limited to XGBoost GBM, XGBoost Dart, XGBoost GLM, LightGBM, RuleFit, Tensorflow, and FTRL models.  The table below explains why certain algorithms were not selected for the final model, if any.

{{alternative_models._algo_selection}}

**Alternative Model Performance**

In this experiment Driverless AI evaluated {{"{:,.0f}".format(alternative_models._num_alternative_models)}} alternate models and {{"{:,.0f}".format(final_features.get_num_transformed_features_survived())}} features. 

{% if validation_schema._ga_disabled %}{% else %}
The plot below shows the alternative models evaluated and their {{experiment.score_f_name}} on the validation data.  The final model corresponds to the point shown for the greatest iteration.
{{ images.get(alternative_models._plots.get('iteration_scores', {} ).get('filename',''))}} {% endif %}

