### Final Model Details

{{final_model._final_model_desc.overview}}

{% for key, value in final_model._details.detailed_params.items()%}

**Model Index: {{key}}**

{{value}}

{% endfor %}


{{section.render('Appendix.PSI_Appendix')}}

{{section.render('Appendix.Response_Rates_Appendix')}}

{{section.render('Appendix.NLP Appendix')}}


{% if (final_model._glm_in_final ) and (final_model._glm_coef_appdx[0]) %}

### GLM Model Coefficients Table

The following section includes the fitted standardized coefficients for the Final Model's GLM(s). The Mean, Variance, and Scales (the standardized value) columns correspond to each feature, and can be used to standardize the dataset.
{% if final_model._glm_coef_appdx[1] %}

{% if (final_model._problem_type == 'multinomial') and (final_model._num_classes > 3) %}

{% for fold_key in final_model._glm_coef_appdx[0] %}

{{ final_model._glm_coef_appdx[0][fold_key][1] }}
{{ final_model._glm_coef_appdx[0][fold_key][2] }}

{% for multic_key in final_model._glm_coef_appdx[0][fold_key][0] %}

{{final_model._glm_coef_appdx[0][fold_key][0][multic_key]}}

{% endfor %}

{% endfor %}

{% else %}

{% for key in final_model._glm_coef_appdx[0] %}

{{ final_model._glm_coef_appdx[0][key][1] }}
{{ final_model._glm_coef_appdx[0][key][2] }}

{{final_model._glm_coef_appdx[0][key][0]}}

{% endfor %}

{% endif %}

{% else %}

{% if  (final_model._problem_type == 'multinomial') and (final_model._num_classes > 3) %}

{% for key in final_model._glm_coef_appdx[0] %}

{{final_model._glm_coef_appdx[0][key]}}

{% endfor %}

{% else %}

{{final_model._glm_coef_appdx[0]}}

{% endif %}

{% endif  %}

{% endif %}

{% if final_model._glm_in_final %}

### Understanding the GLM Coefficients Table

The following section provides insight into how GLM predictions could be constructed from the GLM coefficients table. The equations, however, are not meant for scoring in production – the Python and MOJO scoring pipelines should be used to generate predictions in production.

When the DAI Final Model includes a GLM, DAI provides standardized coefficients for the GLM - these artifacts exist within the experiment summary zip file (ensemble\_glm_coefs\_scalers.json, ensemble\_glm\_coefs\_scalers.tab.txt) and report.docx. These coefficients, along with the provided training data statistics (e.g., Means, Variances, and Scales) can be used to make a GLM outside of DAI.
The following section walks through the steps to construct a GLM, specifically:

1. Transforming test set features
2. Standardizing test set features
3. Generating predictions with the provided standardized coefficients

**Transforming Features**

To transform the test set features, apply the same DAI feature transformations to the test set. Applied transformations are listed in the `Feature Transformation` section of the report.docx and in the experiment summary zip file (features.json, features.txt, features.tab.txt). While transformations like frequency encoding and one-hot encoding are easy to replicate, other proprietary transformations may not be possible. For this reason, we recommend either setting the `Pipeline Building Recipe` to `compliant` or setting the `Feature Engineering Effort` to `1` or `0`.

**Standardizing Features**

To standardize the test set, use the mean and scaling statistics of the training dataset. The necessary training statistics (e.g. mean and scale) are available in the report.docx's GLM coefficients table and in the experiment summary zip file (ensemble\_glm\_coefs\_scalers.json, ensemble\_glm\_coefs\_scalers.tab.txt). These statistics are calculated following the conventions of Scikit-Learn's {{section.link('StandardScaler','https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html')}}, which are as follows:

1. Demean: subtract a feature's mean from each of its values.
2. Scale: divide each feature's value by the standard deviation of the feature.

**Generating Predictions**

The standardized coefficients from the GLM can be used to generate predictions, once the test set is standardized based on the training statistics.
Use the following equations to generate predictions:

For regression:

{% raw %}
$$ \begin{aligned}
\widehat{y} = \mathbf{x^T}\boldsymbol{\beta}+\beta_{\phi}
\end{aligned} $$
{% endraw %}

For binary classification:

{% raw %}
$$ \begin{aligned}
\widehat{y} = Pr(y=1|\mathbf{x}) = \dfrac {e^{\mathbf{x{^T}}\boldsymbol{\beta} + {\beta_0}}} {1 + {e^{\mathbf{x{^T}}\boldsymbol{\beta} + {\beta_0}}}}
\end{aligned} $$
{% endraw %}

For multi-class classification:

{% raw %}
$$ \begin{aligned}
\widehat{y} = Pr(y=c|\mathbf{x}) = \dfrac {e^{\mathbf{x{^T}}\boldsymbol{\beta_c} + {\beta_{\phi c}}}} {1 + \sum_{k=1}^{K-1}{{e^{\mathbf{x{^T}}\boldsymbol{\beta_{k}} + {\beta_{\phi k}}}}}}
\end{aligned} $$

$$ \begin{aligned} 
\widehat{y} = Pr(y=K|\mathbf{x}) = \dfrac {1} {1 + \sum_{k=1}^{K-1}{{e^{\mathbf{x{^T}}\boldsymbol{\beta_{k}} + {\beta_{\phi k}}}}}}
\end{aligned}
$$
{% endraw %}

$$\widehat{y}$$ : the prediction probability

$$y$$ : the class outcome

$$\mathbf{x}$$ : a dataset record or observation

$$\boldsymbol{\beta}$$ : the coefficients

$$\beta_{\phi}$$: the intercept

$$K$$ : the number of classes

$$k$$ : class index

$$c$$ : a class with labels c = 1, 2, …, $$K-1$$

Reference for the GLM equations: *Hastie, Trevor, Robert Tibshirani, and J Jerome H Friedman. The Elements of Statistical Learning. Vol.1. N.p., Springer New York, 2001.*


{% endif %}

{% if params._params.config_overrides != None %}
{% if params._params.config_overrides | length > 0 %}
### Config Overrides

The Config Overrides represent the fine-control parameters.{% if config.autodoc_list_all_config_settings %} Note: the settings listed below do not differentiate between what a user explicitly set and what DAI automatically set.{% endif %}

{{params.get_config_overrides_table()}}
{% endif %}
{% endif %}

{% if reference_list %}
### References

{% if pasting_reference %}{{pasting_ref_num}}. Leo Breiman. 1999. Pasting Small Votes for Classification in Large Databases and On-Line. Mach. Learn. 36, 1-2 (July 1999), 85-103. DOI: https://doi.org/10.1023/A:1007563306331{% endif %}
{% endif %}
