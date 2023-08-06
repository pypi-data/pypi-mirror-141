{% if final_model._glm_in_final %}

**GLM Model Coefficients Table**

The following section includes the fitted standardized coefficients for the Final Model's GLM(s). The Mean, Variance, and Scales (the standardized value) columns correspond to each feature, and can be used to standardize the dataset.

{% if final_model._glm_coef_table[1] %}

{% if (final_model._problem_type == 'multinomial') and (final_model._num_classes > 3) %}

{% for fold_key in final_model._glm_coef_table[0] %}

**{{ final_model._glm_coef_table[0][fold_key][1]|e}}**

**{{ final_model._glm_coef_table[0][fold_key][2]|e}}**

{% for multic_key in final_model._glm_coef_table[0][fold_key][0] %}

{{final_model._glm_coef_table[0][fold_key][0][multic_key]}}

{% endfor %}

{% endfor %}

{% else %}

{% for key in final_model._glm_coef_table[0] %}

**{{ final_model._glm_coef_table[0][key][1]|e}}**

**{{ final_model._glm_coef_table[0][key][2]|e}}**

{{final_model._glm_coef_table[0][key][0]}}

{% endfor %}

{% endif %}

{% else %}

{% if  (final_model._problem_type == 'multinomial') and (final_model._num_classes > 3) %}

{% for key in final_model._glm_coef_table[0] %}

{{final_model._glm_coef_table[0][key]}}

{% endfor %}

{% else %}

{{final_model._glm_coef_table[0]}}

{% endif %}

{% endif  %}

{% endif %}

{% if final_model._glm_coef_appdx[0] %}

The full coefficients table or tables can be found in the Appendix section.

{% else %}

{% endif %}


