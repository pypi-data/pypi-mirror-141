While each class of algorithm has inherent limitations, Driverless AI addresses many of these limitations through feature engineering, hyperparameter tuning, and early stopping. 

{% if  final_model._glm_in_final or  ('RuleFitModel' in final_model._final_model_string )%}

Generalized Linear Models, for example, cannot capture interactions if a feature does not explicitly represent that interaction (e.g., multiplying or adding features). Driverless AI includes feature transformations and generation that represent interactions, to minimize this possible performance drawback.

{% endif %}

{% if ('XGBoostGBMModel' in final_model._final_model_string) or ('LightGBMModel' in final_model._final_model_string) or ('XGBoostDartModel' in final_model._final_model_string) %} 

Gradient Boosting Models, for example, are prone to overfitting if the input dataset is noisy, contains high-cardinality features, or if the algorithm is not tuned properly (i.e., using too many trees or very deep trees). Driverless AI mitigates these potential pitfalls by numerically encoding high-cardinality features, applying best-practices for hyperparameter tuning, and using early stopping, among other measures.

{% endif %}

{% if  'TensorFlowModel' in final_model._final_model_string %}
Neural networks models are prone to overfitting on small datasets. Given enough data, however, a TensorFlow model can fit complex functions with higher accuracy than tree-based algorithms. A TensorFlow model will likely take much longer to converge and is less interpretable when compared to other algorithms.{% endif %}

{% if  'FTRLModel' in final_model._final_model_string %}Warning FTRL models are not supported in this automatic report.{% endif %}


