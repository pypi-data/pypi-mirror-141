**Performance of Final Model**

{{final_model.get_final_model_scores()}}

{% if predictions.cv_performance and final_model.cv_perf_dict %} 

**Per Fold Cross-Validation Metrics**

H2O-3 models provide two different calculations for cross-validation metrics. The first, shown in the above table and plots, is calculated across the aggregated cross-validation predictions; The second provides the average metric (cv mean) across the cross-validation folds (shown below).

{% for key in final_model.cv_perf_dict.keys() %}
{{ final_model.cv_perf_dict.get(key) }}
{% endfor %}{% endif %}

{% if params._params.is_classification and final_model._confusion_matrix != {} %} 
{% for split in final_model._confusion_matrix.keys() %}
{{ section.render('Final Model.Validation_CM_H2O3', split= final_model._confusion_matrix.get(split))}}
{% endfor %}{% endif %}

{% for key, value in final_model._plots.items() %}

**{{ value.desc |e}}**

{{ value.details|e}}

{% for split, filename in value.images.items() %}{{images.get(filename)}}{% endfor %}


{% endfor %} 
