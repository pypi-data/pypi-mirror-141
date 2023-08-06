A model can be explained globally and locally.  A global interpretation of the model describes general patterns found by the model. Tools to understand the model at a global level include:

- Variable importance of final variables

- Variable importance of original variables

- Surrogate models – surrogate decision tree, surrogate linear model

- Partial Dependence Plots

A local interpretation of the model provides background for why a specific record had the prediction that it did.  Tools to understand the model at a local level include:

- Leave One Covariate Out (LOCO)

- K-LIME Reason Codes

- Individual Conditional Expectation Plots (ICE)

When performing local analysis of a model, Partial Dependence Plots (PDP), KLIME Reason Codes, Individual Conditional Expectation (ICE), and Leave-one-covariate-out (LOCO) are machine learning interpretability techniques that together provide a holistic view of the model's results. 

#### Global Interpretation

This section aims to provide a high-level understanding of the patterns in the data that the final Driverless AI model was able to find.

**Variable Importance**

The barchart below shows the top variables from the final model.  {% if final_features.get_num_transformed_features_used() > 0 %} Some of these features were automatically created by Driverless AI. {% endif %} {% if final_features._feature_importance | length > 20 %}The top 20 features used in the final model are shown below, ordered by importance. {% else %} All {{ final_features._feature_importance | length | int }} features used in the final model are shown below ordered by importance. {% endif %} If no transformer was applied, the feature is an original column.  The variable importance shown is the Gain based importance.

{{final_features.get_feature_importance_plot()}}

**Original Variable Importance**

Because some variables were automatically created by Driverless AI, the variable importance barchart shown above may not be fully interpretable.  We also include here the variable importance of the original variables in the model.  This needs to be derived since we do not guarantee that Driverless AI will only use original variables.  We derive the original variable importance using Component Based Variable Importance.

{% if final_features.get_original_feature_importance_plot() == None %}

For this experiment, the original variables had no variable importance since they were not directly used to create any features used in the final model.  For example, the sales from last week uses a date column to be calculated but we do not consider the date column to be directly related to that feature. 

{% else %}

{{ final_features.get_original_feature_importance_plot()}} 

{% endif %}

