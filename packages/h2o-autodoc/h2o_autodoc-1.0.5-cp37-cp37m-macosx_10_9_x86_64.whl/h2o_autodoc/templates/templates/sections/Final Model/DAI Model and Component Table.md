For this experiment,{% if final_model._num_ensemble_models < 1 %} the final model is **{{final_model._final_model_string}}**, which is the best performing model from the feature engineering iterations. {% else %} the final model is a stacked ensemble of  **{{final_model._final_model_string}}**. The features of {% if final_model._num_ensemble_models > 1 %} these models {% else %} this model {% endif %} are the best features found during the feature engineering iterations. {% endif %}

{% if final_model._num_ensemble_models >= 1 %}

**Ensemble Model Structure** 

{% endif %}

This table below shows the components of the final model:

{{section.render('Final Model.DAI Final Model Components Table')}}

