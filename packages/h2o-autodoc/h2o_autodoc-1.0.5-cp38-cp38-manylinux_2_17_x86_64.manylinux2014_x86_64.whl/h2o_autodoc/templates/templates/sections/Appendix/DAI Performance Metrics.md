**R2 (R Squared)** – The R2 value represents the degree that the predicted value and the actual value move in unison. The R2 value varies between 0 and 1 where 0 represents no correlation between the predicted and actual value and 1 represents complete correlation. Calculating the R2 value for linear models is mathematically equivalent to 1−SSE/SST1−SSE/SST (or 1−residual sum of squares/total sum of squares1−residual sum of squares/total sum of squares). For all other models, this equivalence does not hold, so the 1−SSE/SST1−SSE/SST formula cannot be used. In some cases, this formula can produce negative R2 values, which is mathematically impossible for a real number. Because Driverless AI does not necessarily use linear models, the R2 value is calculated using the squared Pearson correlation coefficient.  

**R2** equation:

$$ \begin{aligned}
R2 = \dfrac{\sum_{i=1}^{n}{(x_i-\bar{x})(y_i-\bar{y})}}{\sqrt{\sum_{i=1}^{n}{(x_i-\bar{x})^2}\sum_{i=1}^{n}{(y_i-\bar{y})^2}}}
\end{aligned} $$

Where:

$x$ is the predicted target value

$y$ is the actual target value


**GINI (Gini Coefficient)** – The Gini index is a well-established method to quantify the inequality among values of a frequency distribution, and can be used to measure the quality of a binary classifier. A Gini index of zero expresses perfect equality (or a totally useless classifier), while a Gini index of one expresses maximal inequality (or a perfect classifier). The Gini index is based on the Lorenz curve. The Lorenz curve plots the true positive rate (y-axis) as a function of percentiles of the population (x-axis). The Lorenz curve represents a collective of models represented by the classifier. The location on the curve is given by the probability threshold of a particular model. (i.e., Lower probability thresholds for classification typically lead to more true positives, but also to more false positives.) The Gini index itself is independent of the model and only depends on the Lorenz curve determined by the distribution of the scores (or probabilities) obtained from the classifier. {% if params._params.is_classification %}

**MCC (Matthews Correlation Coefficient)** - The goal of the MCC metric is to represent the confusion matrix of a model as a single number. The MCC metric combines the true positives, false positives, true negatives, and false negatives using the equation described below.  A Driverless AI model will return probabilities, not predicted classes. To convert probabilities to predicted classes, a threshold needs to be defined. Driverless AI iterates over possible thresholds to calculate a confusion matrix for each threshold. It does this to find the maximum MCC value. Driverless AI’s goal is to continue increasing this maximum MCC.  Unlike metrics like Accuracy, MCC is a good scorer to use when the target variable is imbalanced. In the case of imbalanced data, high Accuracy can be found by simply predicting the majority class. Metrics like Accuracy and F1 can be misleading, especially in the case of imbalanced data, because they do not consider the relative size of the four confusion matrix categories. MCC, on the other hand, takes the proportion of each class into account. The MCC value ranges from -1 to 1 where -1 indicates a classifier that predicts the opposite class from the actual value, 0 means the classifier does no better than random guessing, and 1 indicates a perfect classifier.

**F05, F1**, and **F2**: A Driverless AI model will return probabilities, not predicted classes. To convert probabilities to predicted classes, a threshold needs to be defined. Driverless AI iterates over possible thresholds to calculate a confusion matrix for each threshold. It does this to find the maximum some F metric value. Driverless AI’s goal is to continue increasing this maximum F metric.

**Accuracy**: In binary classification, Accuracy is the number of correct predictions made as a ratio of all predictions made. In multiclass classification, the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true. A Driverless AI model will return probabilities, not predicted classes. To convert probabilities to predicted classes, a threshold needs to be defined. Driverless AI iterates over possible thresholds to calculate a confusion matrix for each threshold. It does this to find the maximum Accuracy value. Driverless AI’s goal is to continue increasing this maximum Accuracy.

**Logloss**: The logarithmic loss metric can be used to evaluate the performance of a binomial or multinomial classifier. Unlike AUC which looks at how well a model can classify a binary target, logloss evaluates how close a model’s predicted values (uncalibrated probability estimates) are to the actual target value. For example, does a model tend to assign a high predicted value like .80 for the positive class, or does it show a poor ability to recognize the positive class and assign a lower predicted value like .50? Logloss ranges between 0 and 1, with 0 meaning that the model correctly assigns a probability of 0% or 100%.

**AUC (Area Under the Receiver Operating Characteristic Curve)** -This model metric is used to evaluate how well a binary classification model is able to distinguish between true positives and false positives. An AUC of 1 indicates a perfect classifier, while an AUC of .5 indicates a poor classifier whose performance is no better than random guessing. Driverless AI uses the trapezoidal rule to approximate the area under the ROC curve. 

**AUCPR (Area under the Precision-Recall Curve)** - This model metric is used to evaluate how well a binary classification model is able to distinguish between precision recall pairs or points. These values are obtained using different thresholds on a probabilistic or other continuous-output classifier. AUCPR is an average of the precision-recall weighted by the probability of a given threshold. {% else %}

**MSE (Mean Squared Error)** - The MSE metric measures the average of the squares of the errors or deviations. MSE takes the distances from the points to the regression line (these distances are the “errors”) and squaring them to remove any negative signs. MSE incorporates both the variance and the bias of the predictor.  MSE also gives more weight to larger differences. The bigger the error, the more it is penalized. For example, if your correct answers are 2,3,4 and the algorithm guesses 1,4,3, then the absolute error on each one is exactly 1, so squared error is also 1, and the MSE is 1. But if the algorithm guesses 2,3,6, then the errors are 0,0,2, the squared errors are 0,0,4, and the MSE is a higher 1.333. The smaller the MSE, the better the model’s performance

**MSE** equation: 

$$ \begin{aligned}
MSE = \dfrac{1}{N}\sum_{i=1}^N{(y_i -\widehat{y})^2}
\end{aligned} $$

RMSE (Root Mean Squared Error) - The RMSE metric evaluates how well a model can predict a continuous value. The RMSE units are the same as the predicted target, which is useful for understanding if the size of the error is of concern or not. The smaller the RMSE, the better the model’s performance. 

**RMSE** equation: 
$$ \begin{aligned}
RMSE = \sqrt{\dfrac{1}{N}\sum_{i=1}^N{(y_i -\widehat{y})^2}}
\end{aligned} $$


Where:

$N$ is the total number of rows (observations) of your corresponding dataframe.

$y$ is the actual target value.

$\widehat{y}$ is the predicted target value.

**RMSLE (Root Mean Squared Logarithmic Error)** - This metric measures the ratio between actual values and predicted values and takes the log of the predictions and actual values. Use this instead of RMSE if an under-prediction is worse than an over-prediction. You can also use this when you don’t want to penalize large differences when both of the values are large numbers.

**RMSLE** equation: 

$$ \begin{aligned}
RMSLE = \sqrt{\dfrac{1}{N}\sum_{i=1}^N{(ln(\dfrac{y_i + 1}{\widehat{y_i} + 1}))^2}}
\end{aligned} $$

Where:

$N$ is the total number of rows (observations) of your corresponding dataframe.

$y$ is the actual target value.

$\widehat{y}$ is the predicted target value.

**RMSPE (Root Mean Squared Percent Error)** - This metric is the RMSE expressed as a percentage. The smaller the RMSPE, the better the model performance.

**RMSPE** equation:

$$ \begin{aligned}
RMSPE = \sqrt{ \dfrac{1}{N}\sum_{i=1}^N{ \dfrac{(y_i - \widehat{y_i})^2}{ {y_i}^2} } } * 100 
\end{aligned} $$

Where:

$N$ is the total number of rows (observations) of your corresponding dataframe.

$y$ is the actual target value.

$\widehat{y}$ is the predicted target value.

**MAE (Mean Absolute Error)** - The mean absolute error is an average of the absolute errors. The MAE units are the same as the predicted target, which is useful for understanding whether the size of the error is of concern or not. The smaller the MAE the better the model’s performance. (Tip: MAE is robust to outliers. If you want a metric that is sensitive to outliers, try root mean squared error (RMSE).)

**MAE** equation:

$$ \begin{aligned}
MAE = \dfrac{1}{N}\sum_{i=1}^N{|y_i - \widehat{y_i}|}
\end{aligned} $$


Where:

$N$ is the total number of rows (observations) of your corresponding dataframe.

$y$ is the actual target value.

$\widehat{y}$ is the predicted target value.

**MAPE (Mean Absolute Percent Error)** - MAPE measures the size of the error in percentage terms. It is calculated as the average of the unsigned percentage error.

**MAPE** equation:

$$ \begin{aligned}
MAPE = (\dfrac{1}{N}\sum_{i=1}^N{\dfrac{|y_i - \widehat{y_i}|}{|y_i|}}) * 100
\end{aligned} $$

Where:

$N$ is the total number of rows (observations) of your corresponding dataframe.

$y$ is the actual target value.

$\widehat{y}$ is the predicted target value.

**SMAPE (Symmetric Mean Absolute Percent Error)** - Unlike the MAPE, which divides the absolute errors by the absolute actual values, the SMAPE divides by the mean of the absolute actual and the absolute predicted values. This is important when the actual values can be 0 or near 0. Actual values near 0 cause the MAPE value to become infinitely high. Because SMAPE includes both the actual and the predicted values, the SMAPE value can never be greater than 200%.

**MER (Median Absolute Error Rate)** - MER measures the median size of the error in percentage terms. It is calculated as the median of the unsigned percentage error.

**MER** equation:

$$ \begin{aligned}
MER = (median({\dfrac{|y_i - \widehat{y_i}|}{|y_i|}})) * 100
\end{aligned} $$


Where:

$y$ is the actual target value.

$\widehat{y}$ is the predicted target value.{% endif %}
