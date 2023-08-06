{% if package_name=='Scikit-learn' %}The feature importance table shows the model-specific variable importance (Native Importance) and Scaled Native Importance (where values are scaled between 0 and 1).{% else%}{{package_name}} models provide built-in variable importance (Native Importance) and can provide Shapley Importance for supported algorithms.

* **Native Importance:** Model-specific variable importance calculated with H2O-3's varimp() function (H2O-3 documentation details __{{ final_model.doc_url_varimp }}__). 

* **Scaled Native Importance:** Native Importance scaled between 0 and 1.

* **Shapley:** The mean absolute Shapley value of a feature, using TreeSHAP (SHAP documentation details __{{ final_model.doc_shap_url }}__).

* **Relative Shapley:** The feature's mean absolute Shapley value divided by the largest Shapley value.
{% endif %}
