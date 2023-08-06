{% if final_model.mc_available %}**Monotonicity Constraints Details**

Monotonicity constraints enforce a monotonic relationship between a specified feature and the target prediction. For example, given a model trained to predict housing prices, we might want to enforce that the model predicts higher housing prices with increasing lot size and lower housing prices with increasing neighborhood crime rate.

{% if final_model.uses_monotonic_gbm %}This experiment uses the Monotonic GBM Recipe to enforce an overall monotonic modeling pipeline, where monotonicity constraints are respected in the feature engineering and fitted model steps. In this recipe, all numeric features with an absolute correlation less than {{ config.monotonicity_constraints_correlation_threshold }} are dropped and ensembles are turned off to help reduce model complexity.{% elif final_model.automatic_monotonicity_constraints %}This experiment enables automatic monotonicity constraints, which mean Driverless AI automatically determines if monotonicity is present and then enforces it through all or part of the modeling pipelines. Depending on the level of feature-target correlation, Driverless AI assigns positive, negative, or no monotonicity constraints. Specifically, monotonicity constraints are enforced if the absolute correlation is greater than {{ config.monotonicity_constraints_correlation_threshold }} (the monotonicity correlation threshold set for this experiment). Driverless AI does not enforce monotonicity constraints for features below this correlation threshold.{% endif %}

{% if final_model.user_monotonicity_constraints %}**User-Define Monotonicity Constraints**

Driverless AI enforces the user-defined monotonicity constraint configuration in the feature engineering pipeline and for the fitted models.  

{{ final_model.user_monotonicity_constraints }}

{% for feature, info in pdp.monotonic_feature_pdps.items() %}

Feature {{feature|e}}{{ info["rendered_image"]}}

{% endfor %}{% endif %}{% endif %}



