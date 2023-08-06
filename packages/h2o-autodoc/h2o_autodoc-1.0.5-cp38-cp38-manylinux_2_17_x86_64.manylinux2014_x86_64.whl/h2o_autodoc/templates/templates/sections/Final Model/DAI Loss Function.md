The experiment’s overall goal is to optimize the selected scorer: **{{ experiment.score_f_name }}**.  Every model trained is evaluated on the {{ experiment.score_f_name }} performance on validation data.  The experiment will complete once new models do not show significant improvement in the validation {{ experiment.score_f_name }}.

The selected scorer will influence parameter tuning, feature selection, feature engineering and final model creation.  At the individual model level, however, the loss function that is optimized is not {{ experiment.score_f_name }}.  Instead, the loss function is chosen based on the available loss functions for the algorithm and the type of use case (regression, binomial, multinomial).   

The table below shows the loss functions that are optimized for {% if final_model._num_ensemble_models > 0 %} each model in the final stacked ensemble. {% else %} the final model. 

{% endif %}

{{section.render('Final Model.DAI Model Objective Table')}}

{% if 'TensorFlowModel' in final_model._final_model_string %}TensorFlows "auto" objective function maps to the categorical cross-entropy objective function for classification problems and mean squared error for regression problems.{% endif %}

{% if params._params.is_classification == False %} 

For regression, Tweedie/Gamma/Poisson/etc. regression is not yet supported, but Driverless AI handles various target transforms so many target distributions can be handled very effectively already. Driverless AI handles quantile regression for alpha=0.5 (media), and general quantiles are on the roadmap. 

{% endif %}
