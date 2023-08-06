**Performance of Final Model**

{{final_model.get_final_model_scores()}}

{% if params._params.is_classification and final_model._confusion_matrix != {} and "validation" in final_model._confusion_matrix.keys()%}

**Validation Confusion Matrix**

{%if final_model.valid_cm_threshold| e == 'argmax' %}The prediction label is assigned to the class with the highest predicted probability.{% else %}*Threshold {{final_model.valid_cm_threshold}}*{% endif %}

{{final_model._confusion_matrix.validation}}

{% endif %} 

{% if params._params.is_classification and experiment.test_score != None  and final_model._confusion_matrix != {} %}

**Test Confusion Matrix**

{%if final_model.test_cm_threshold| e == 'argmax' %}The prediction label is assigned to the class with the highest predicted probability.{% else %}*Threshold {{final_model.test_cm_threshold}}*{% endif %}

{{final_model._confusion_matrix.test}}

{% endif %}

{% if experiment.test_score == None %}

{% for key, value in final_model._plots.items() %}

**{{value.desc}}**

{% if value.desc == 'Receiver Operating Characteristic Curve' %}

The graph shows Receiver Operating Characteristic Curve statistics. The area under this curve is called the AUC. The True Positive Rate (TPR) is the relative fraction of correct positive predictions, and the False Positive Rate (FPR) is the relative fraction of incorrect positive corrections. Each point corresponds to a classification threshold (e.g., YES if probability >= 0.3 else NO). For each threshold, there is a unique confusion matrix that represents the balance between TPR and FPR. Most useful operating points are in the top left corner in general.

{% elif value.desc == 'Precision Recall Curve' %}

Each point corresponds to a classification threshold (e.g., YES if probability >= 0.3 else NO). For each threshold, there is a unique confusion matrix that represents the balance between Recall and Precision. This ROCPR curve can be more insightful than the ROC curve for highly imbalanced datasets.

{% elif value.desc == 'Cumulative Lift' %}

This chart shows the Cumulative Lift. For example, "How many more times are the observations of the positive target class in the top predicted 1%, 2%, 10%, etc. (cumulative) compared to randomly selected observations?" By definition, the Lift at 100% is 1.0.

{% elif value.desc == 'Cumulative Gains' %}

This shows the Cumulative Gains. For example, "What fraction of all observations of the positive target class are in the top predicted 1%, 2%, 10%, etc. (cumulative)?" By definition, the Gains at 100% are 1.0. {% elif value.desc == 'Kolmogorov–Smirnov' %}The Kolmogorov–Smirnov statistic shows the difference between the cumulative portion of correct predictions and the cumulative portion of incorrect predictions across different prediction quantiles.  The greater the K-S statistic, the greater the portion of correctly classified predictions.

{% elif value.desc == 'Actual vs Predicted' %}

An Actual vs. Predicted table displays for Regression experiments. This shows Actual vs Predicted values on validation data. A small sample of values are displayed. A perfect model has a diagonal line.

{% endif %}

{{ images.get(value.validation_filename)}}

{% endfor %}

{% else %}

{% for key, value in final_model._plots.items() %}

**{{value.desc}}**

{% if value.desc == 'Receiver Operating Characteristic Curve' %}

This shows Receiver Operating Characteristic Curve stats on validation data. The area under this curve is called the AUC. The True Positive Rate (TPR) is the relative fraction of correct positive predictions, and the False Positive Rate (FPR) is the relative fraction of incorrect positive corrections. Each point corresponds to a classification threshold (e.g., YES if probability >= 0.3 else NO). For each threshold, there is a unique confusion matrix that represents the balance between TPR and FPR. Most useful operating points are in the top left corner in general.

{% elif value.desc == 'Precision Recall Curve' %}Each point corresponds to a classification threshold (e.g., YES if probability >= 0.3 else NO). For each threshold, there is a unique confusion matrix that represents the balance between Recall and Precision. This ROCPR curve can be more insightful than the ROC curve for highly imbalanced datasets.

{% elif value.desc == 'Cumulative Lift' %}This chart shows the Cumulative Lift. For example, "How many times more observations of the positive target class are in the top predicted 1%, 2%, 10%, etc. (cumulative) compared to selecting observations randomly?" By definition, the Lift at 100% is 1.0.

{% elif value.desc == 'Cumulative Gains' %}This shows the Cumulative Gains. For example, "What fraction of all observations of the positive target class are in the top predicted 1%, 2%, 10%, etc. (cumulative)?" By definition, the Gains at 100% are 1.0.

{% elif value.desc == 'Kolmogorov–Smirnov' %}The Kolmogorov–Smirnov statistic shows the difference between the cumulative portion of correct predictions and the cumulative portion of incorrect predictions across different prediction quantiles.  The greater the K-S statistic, the greater the portion of correctly classified predictions.

{% elif value.desc == 'Actual vs Predicted' %}An Actual vs. Predicted table displays for Regression experiments. This shows Actual vs Predicted values on validation data. A small sample of values are displayed. A perfect model has a diagonal line.

{% endif %}

{{ images.get(value.validation_filename)}}{{ images.get(value.test_filename)}}

{% endfor %}

{% endif %}

