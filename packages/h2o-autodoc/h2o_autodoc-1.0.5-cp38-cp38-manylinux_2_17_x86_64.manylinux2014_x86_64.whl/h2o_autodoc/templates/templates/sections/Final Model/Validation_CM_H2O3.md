**{{split.info[0]}}**

The confusion matrix shows how many observations the model correctly classified and misclassified.{% if package_name=='H2O-3' %} The first column contains the actual class labels; the first row contains the predicted class labels.{% endif %} 

{% if predictions.problem_type.value == 'binary' and  package_name=='H2O-3' %}A positive prediction label (e.g., 1, True, or the second label in lexicographical order), is assigned to all observations where the predicted probability is greater than or equal to {{ split.info[2]}} (the threshold for the highest F1 score on the {{split.info[1]}} dataset).{% elif predictions.problem_type.value == 'binary' and  package_name=='Scikit-learn' %}A positive prediction label is assigned to all observations where the predicted probability is greater than .5.{% else %}The prediction label is assigned to the class with the highest predicted probability. {% endif %}

{{ split.image }}

{{ split.cm }}

