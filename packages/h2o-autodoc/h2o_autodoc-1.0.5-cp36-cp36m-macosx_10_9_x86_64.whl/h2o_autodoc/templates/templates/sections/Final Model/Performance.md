**Performance of Final Model**

{{final_model.get_final_model_scores()}}

{% if params._params.is_classification and final_model._confusion_matrix != {} and "validation" in final_model._confusion_matrix.keys()%}

**Validation Confusion Matrix**

{%if final_model.valid_cm_threshold| e == 'argmax' %}The prediction label is assigned to the class with the highest predicted probability.{% else %}*Threshold {{final_model.valid_cm_threshold}}*{% endif %}

{{final_model._confusion_matrix.validation}}

{%endif %} 

{% if params._params.is_classification and experiment.test_score != None  and final_model._confusion_matrix != {} %} 

**Test Confusion Matrix**

{%if final_model.test_cm_threshold| e == 'argmax' %}The prediction label is assigned to the class with the highest predicted probability.{% else %}*Threshold {{final_model.test_cm_threshold}}*{% endif %}

{{final_model._confusion_matrix.test}}

{% endif %} 

{% if experiment.test_score == None %}

{% for key, value in final_model._plots.items() %}

*{{ value.desc |e}}*

{{ images.get(value.validation_filename)}}


{% endfor %} {% else %} 

{% for key, value in final_model._plots.items() %}

*{{ value.desc |e}}*

{{ images.get(value.validation_filename, '')}}
{{ images.get(value.test_filename, '')}}

{% endfor %} 

{% endif %}
