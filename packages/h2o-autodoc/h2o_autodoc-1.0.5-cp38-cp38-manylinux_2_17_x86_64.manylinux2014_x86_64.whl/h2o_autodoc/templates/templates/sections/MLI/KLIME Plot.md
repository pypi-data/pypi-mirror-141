The plot below shows the GLM surrogates’ prediction, the Driverless AI model prediction, and the actual target value along the y-axis.  The records are ordered based on their Driverless AI prediction.  The plot shows how well the GLM surrogates can predict the Driverless AI model.  (The closer the GLM surrogate predictions are to the Driverless AI model predictions, the better the fit of the GLM surrogates).

The GLM surrogate prediction for each record may be from either the global surrogate GLM or the local surrogate GLM trained on their cluster.  If the local surrogate GLM has a lower R2 value than the global surrogate GLM, the global surrogate GLM is used for the records in that cluster.

{{images.get('klime_global')}}

