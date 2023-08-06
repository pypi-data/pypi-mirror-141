{% if validation_schema._feature_evolution_enabled %}{% if validation_schema._model_n_feature_tuning_enabled %}During the Model and Feature Tuning Stage, Driverless AI evaluates the effects of different types of algorithms, algorithm parameters, and features. The goal of the Model and Feature Tuning Stage is to determine the best algorithm and parameters to use during the Feature Evolution Stage.{% endif %}

In the Feature Evolution Stage, Driverless AI trained {{feature_evolution._feature_evolution_algos|e}} ({{experiment_overview._stage_info.get("Feature evolution", {"models": "models"}).models}}) where each model evaluated a different set of features. The Feature Evolution Stage uses a genetic algorithm to search the large feature engineering space.

The graph below shows the effect the {% if validation_schema._model_n_feature_tuning_enabled %} Model and Feature Tuning Stage and {% endif %}
Feature Evolution Stage had on the performance.

{{ images.get(alternative_models._plots.iteration_scores.filename)}}  

Based on the experiment settings and column types in the dataset, Driverless AI was able to explore the following transformers: 

{% for key, value in feature_evolution._feature_transformers_available.items() %}

- **{{key|e}}**: {{value|e}}{% endfor %}

{% else %}The goal of the Feature Evolution stage is to determine the best features to use for the final model.  This experiment did not perform the Feature Evolution stage due to the experiment's configurations. {% endif %}

{% set dropped_features_formatted = final_features.get_dropped_features_formatted() %}{% if dropped_features_formatted %}**Dropped Features**

Below is the complete list of dropped features due to numerous reasons.

{{final_features.get_dropped_features_formatted()}}

{% endif %}