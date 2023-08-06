Model simplicity is defined by the user’s accuracy and interpretability setting.  In this case, the experiment’s accuracy was set to {{params._params.accuracy}} and the interpretability was set to {{params._params.interpretability}}.  The interpretability controls the: level of variable selection, monotonicity constraints, and feature transformers available.  The accuracy and interpretability control the complexity of the final model.

For this experiment, the accuracy and interpretability settings effected the experiment in the following ways:

- {% if experiment_overview._internal_args.strategy %}Variable selection was turned on with {{feature_evolution.get_autodoc_varimp_threshold()}} variable selection threshold.{% else %} Variable selection was turned off. {% endif %}

- {% if (experiment_overview._internal_args.monotonicity_constraints) and ('XGBoostGBMModel' in final_model._ensemble_json.get("ensemble_model_description.json").get("Type").values()) or ('XGBoostDartModel' in final_model._ensemble_json.get("ensemble_model_description.json").get("Type").values()) %}Monotonicity constraints were turned on. Driverless AI evaluates the relationship between the predictors and the target variable and enforces monotonicity if the correlation is above a certain threshold. {% elif 'GLMModel' in final_model._ensemble_json.get("ensemble_model_description.json").get("Type").values() %}{% else %}Monotonicity constraints were turned off. {% endif %} 

- Feature transformers available: {{feature_evolution._feature_transformers_available.keys() | join(', ')}}

- Complexity of the final model: {% if experiment_overview._internal_args.ensemble_level == 0 %} a single model {% elif experiment_overview._internal_args.ensemble_level == 1 %}  1x 4-fold models ensembled together {% elif experiment_overview._internal_args.ensemble_level == 2 %}  2x 5-fold models ensembled together {% elif experiment_overview._internal_args.ensemble_level == 3 %}  5x 5-fold models ensembled together {% elif experiment_overview._internal_args.ensemble_level == 4 %}  8x 5-fold models ensembled together {% endif %}

