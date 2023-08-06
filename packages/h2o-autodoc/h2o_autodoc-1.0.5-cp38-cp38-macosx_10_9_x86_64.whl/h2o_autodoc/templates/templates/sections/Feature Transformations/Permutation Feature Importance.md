{% if config. autodoc_include_permutation_feature_importance %}{% if  config. autodoc_feature_importance_scorer %}

**Permutation based feature importance computed using {{feature_importance._score_f_name}} scorer.**

Permutation-based feature importance shows how much a model's performance would change if a feature's values were permuted. If the feature has little predictive power, shuffling its values should have little impact on the model's performance. If a feature is highly predictive, however, shuffling its values should decrease the model's performance. The difference, between the model's performance before and after permuting the feature, provides the feature's absolute permutation importance. For this permutation importance calculation, each feature was shuffled {{config. autodoc_feature_importance_num_perm}} time{% if config. autodoc_feature_importance_num_perm == 1%}.{% else %}s.{% endif %}

{% else %}

**Permutation based feature importance computed using the default model scorer.**

Permutation-based feature importance shows how much a model's performance would change if a feature's values were permuted. If the feature has little predictive power, shuffling its values should have little impact on the model's performance. If a feature is highly predictive, however, shuffling its values should decrease the model's performance. The difference, between the model's performance before and after permuting the feature, provides the feature's absolute permutation importance. For this permutation importance calculation, each feature was shuffled {{config. autodoc_feature_importance_num_perm}} time{% if config. autodoc_feature_importance_num_perm == 1%}.{% else %}s.{% endif %}{% endif %}

{{feature_importance.get_feature_importance_table()}}

**Relative Feature Importance Plot**

{{feature_importance.get_plot(20)}}

{% endif %}

