{% if params._params.is_classification %}

Driverless AI did not perform any target transformations because the experiment was a classification problem.

{% elif (params._params.is_classification == False) and (model_tuning._target_tuning == None) %}

Based on the experiment's accuracy setting, Driverless AI did not apply any target transformations. As a consequence, model performance may suffer, as Driverless AI is optimized for targets with a Gaussian distribution.

{% elif  (params._params.is_classification == False) and (model_tuning._target_tuning != None) %}

For this regression problem, Driverless AI performed target tuning to determine the best way to represent the target column (for example: checking if the log transform of the target could generate better results). For the  *{{experiment.description}}* experiment, Driverless AI tested the following target transformation(s):

{% for item in model_tuning._target_tuning.transformers_used %}

- {{ item }}

{% endfor %}

{% else %}

{% endif %}