**Target Transform Tuning**

{% if params._params.is_classification == False %} {% if model_tuning._target_tuning.transformers_used %}

Driverless AI performed target transform tuning for this regression problem.  Target tuning can improve the performance of the model.  For example, if the target has a positively skewed distribution, taking the log transform may improve the results of the models.  The following table displays how different Driverless AI models performed when different target transformations were applied.


{{model_tuning._target_tuning.table}}

{% else %}

Target tuning can improve the performance of the model.  For example, if the target has a positively skewed distribution, taking the log transform may improve the results of the models.  Driverless AI, however, did not perform target transform tuning for this regression problem because of low accuracy setting.

{% endif %}{% else %}

Driverless AI did not perform target transform tuning because the experiment was classification. 

{% endif %}
