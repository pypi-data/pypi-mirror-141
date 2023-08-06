The result of the Feature Evolution Stage is a set of features to use for the final model.{% if final_features.get_num_transformed_features_used() > 0 %} Some of these features were automatically created by Driverless AI.{% endif %}{% if config.autodoc_num_features != None or config.autodoc_min_relative_importance != None %} The top features used in the final model are shown below, ordered by importance. {% if config.autodoc_num_features != None and config.autodoc_min_relative_importance != None %}The features in the table{% if config.autodoc_num_features == -1%} include all features {% else %} are limited to the top {{config.autodoc_num_features}}{% endif %}, restricted to those with relative importance greater than or equal to {{config.autodoc_min_relative_importance}}. {% elif config.autodoc_num_features != None and config.autodoc_min_relative_importance == None %}The features in the table{% if config.autodoc_num_features == -1%} include all features {% else %} are limited to the top {{config.autodoc_num_features}} {% endif %}. {% elif config.autodoc_num_features == None and config.autodoc_min_relative_importance != None %} The features in the table are limited to those with relative importance greater than or equal to {{config.autodoc_min_relative_importance}}. {% endif %} {% endif %} {% if config.autodoc_num_features == None and config.autodoc_min_relative_importance == None %} All {{ final_features._feature_importance | length | int }} features used in the final model are shown below ordered by importance. {% endif %} If no transformer was applied, the feature is an original column. 

{{section.render('Feature Transformations.Feature Importance')}}

{% if final_model.rulefit_rules %}{% set rule_info = final_model.rulefit_rules %}

**RuleFit Model Rules**

The rules for each RuleFit Model are shown below (rule information is shown with respect to the experiment's artifacts, which are found in the experiment summary zip file).{%- for filename, coef_rule_dict in rule_info.items() %}
* *{{ filename }} artifact:*{%- for key in coef_rule_dict.get("rules_dict", {}).keys() %}

**Coefficient:** {{ coef_rule_dict.get("coef_dict", {}).get(key) }}
**Rule:** {{ coef_rule_dict.get("rules_dict", {}).get(key) }}
{% endfor %}
{% endfor %}{% endif %}
