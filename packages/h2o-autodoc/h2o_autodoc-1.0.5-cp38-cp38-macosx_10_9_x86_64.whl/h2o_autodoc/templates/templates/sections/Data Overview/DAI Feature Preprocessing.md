For the *{{experiment.description}}* experiment, Driverless AI built {% if final_model._num_ensemble_models > 0 %} a Stacked Ensemble ({{final_model._final_model_string}}).{% else %}{{final_model._final_model_string}}. {% endif %}  The following section describes any relevant standardization for this final model: {% if final_model._glm_in_final or ('RuleFitModel' in final_model._final_model_string) %}

For Generalized Linear Models the training dataset is standardized, and that standardization is applied to the validation and test frames.

{% endif %}

{% if 'TensorFlowModel' in final_model._final_model_string %}

For TensorFlow the input dataset is standardized, and the standardization is applied per batch.

{% endif %}

{% if ('XGBoostGBMModel' in final_model._final_model_string) or ('LightGBMModel' in final_model._final_model_string) or ('XGBoostDartModel' in final_model._final_model_string) %}

No standardization is applied for Gradient Boosting Models.

{% endif %}

{% if  'FTRLModel' in final_model._final_model_string %}

Warning FTRL models are not supported in this automatic report.

{% endif %}
