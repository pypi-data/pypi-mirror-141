#### Shapley Contributions on the {{ shap.get_shap_split }} Dataset

Shapley explanations are a technique with credible theoretical support that presents consistent global and local feature contributions. For regression problems, local Shapley feature contributions plus the bias term sum to the final model's prediction. For classification problems, they sum to the prediction before applying the link function.

This section uses Driverless AI's Naive Shapley method to calculate local Shapley explanations for original features. These explanations are approximation for the original features and are based on how often the features are used in transformed features, and how important those transformed features are to the final model. The importance of each transformed feature is distributed equally to all original features that helped create it. This is then summed for each original feature.

{% if shap.sampling_enabled %}The following Shapley summary plot is created from a random sample of {{ config.autodoc_pd_max_rows }} rows (the autodoc_pd_max_rows configuration controls random sampling for this plot).{% endif %}
{{ shap.get_shap_fimp_scatter_plot }}

#### {% if shap._individual_rows %}{% if final_model.target_transformer %}Target Transformation

Driverless AI applied its {{ final_model.target_transformer }} transformer to the target.{% else %}{% endif %}

#### User-Selected Rows

Shapley contributions are shown below for the following user-selected rows: {{ shap._individual_rows }} 
{% for row, row_info in shap.shap_row_info.items() %}

{{ row_info["shap_row_pred"] }}

{{ row_info["shap_contrib_table"] }}

{% endfor %}{% endif %}
