{% if params._params.is_classification %}**Gini Coefficient** - The
Gini index is a well-established method to quantify the inequality among
values of a frequency distribution and can be used to measure the
quality of a binary classifier. A Gini index of 0 expresses perfect
equality (or a totally useless classifier), while a Gini index of 1
expresses a maximal inequality (or a perfect classifier).

The Gini index is based on the Lorenz curve. The Lorenz curve plots the
true positive rate (y-axis) as a function of percentiles of the
population (x-axis).

The Lorenz curve represents a collective of models represented by the
classifier. The location on the curve is given by the probability
threshold for a model. (i.e., lower probability thresholds for
classification typically lead to more true positives, but also to more
false positives.)

The Gini index itself is independent of the model and only depends on
the Lorenz curve determined by the distribution of the scores (or
probabilities) obtained from the classifier.

**Absolute MCC (Matthews Correlation Coefficient)** - Setting
the *absolute\_mcc* parameter sets the threshold for the model's
confusion matrix to a value that generates the highest Matthews
Correlation Coefficient. The MCC score provides a measure of how well a
binary classifier detects true and false positives, and true and false
negatives. The MCC is called a correlation coefficient because it
indicates how correlated the actual and predicted values are; 1
indicates a perfect classifier, -1 indicates a classifier that predicts
the opposite class from the actual value, and 0 means the classifier
does no better than random guessing.

$$\text{MCC} = \frac{TP\ x\ TN - FP\ x\ FN}{\sqrt{(TP + FP)(TP + FN)(TN + FP)(TN + FN)}}$$

**F1** - The F1 score provides a measure for how well a binary
classifier can classify positive cases (given a threshold value). The F1
score is calculated from the harmonic mean of the precision and recall.
An F1 score of 1 means both precision and recall are perfect, and the
model correctly identified all the positive cases and didn't mark a
negative case as a positive case. If either precision or recall are very
low, it will be reflected with a F1 score closer to 0.

$$F1 = 2\frac{(precision)(recall)}{precision + recall}$$

Where:

-   **precision** is the positive observations (true positives) the
    model correctly identified from all the observations it labeled as
    positive (the true positives + the false positives).

-   **recall** is the positive observations (true positives) the model
    correctly identified from all the actual positive cases (the true
    positives + the false negatives).

**F0.5** - The F0.5 score is the weighted harmonic mean of the precision
and recall (given a threshold value). Unlike the F1 score, which gives
equal weight to precision and recall, the F0.5 score gives more weight
to precision than to recall. More weight should be given to precision
for cases where false positives are considered worse than false
negatives. For example, if your use case is to predict which products
you will run out of, you may consider false positives worse than false
negatives. In this case, you want your predictions to be very precise
and only capture the products that will run out. If you predict a
product will need to be restocked when it doesn't, you incur cost by
having purchased more inventory than you need.

$$F0.5 = 1.25\frac{(precision)(recall)}{0.25 precision + recall}$$

Where:

-   **precision** is the positive observations (true positives) the
    model correctly identified from all the observations it labeled as
    positive (the true positives + the false positives).

-   **recall** is the positive observations (true positives) the model
    correctly identified from all the actual positive cases (the true
    positives + the false negatives).

**F2** - The F2 score is the weighted harmonic mean of the precision and
recall (given a threshold value). Unlike the F1 score, which gives equal
weight to precision and recall, the F2 score gives more weight to recall
(penalizing the model more for false negatives then false positives). An
F2 score ranges from 0 to 1, with 1 being a perfect model.

$$F2 = 5\frac{(precision)(recall)}{4 precision + recall}$$

**Accuracy** - In binary classification, Accuracy is the number of
correct predictions made as a ratio of all predictions made. In
multiclass classification, the set of labels predicted for a sample must
exactly match the corresponding set of labels in *y\_true*.

$$\text{Accuracy} = \frac{\text{number correctly predicted}}{\text{number of observations}}$$

**Logloss** - The logarithmic loss metric can be used to evaluate the
performance of a binomial or multinomial classifier. Unlike AUC which
looks at how well a model can classify a binary target, logloss
evaluates how close a model's predicted values (uncalibrated probability
estimates) are to the actual target value. For example, does a model
tend to assign a high predicted value like .80 for the positive class,
or does it show a poor ability to recognize the positive class and
assign a lower predicted value like .50? Logloss can be any value
greater than or equal to 0, with 0 meaning that the model correctly
assigns a probability of 0% or 100%.

Binary classification equation:

$$Logloss = - \frac{1}{N}\sum_{i = 1}^{N}{w_{i}\left( y_{i\ }ln(p_{i} \right) + \left( 1 - y_{\text{i\ }} \right)\ln\left( 1 - p_{i} \right))}$$

Multiclass classification equation:

$$Logloss = - \frac{1}{N}\ \sum_{i = 1}^{N}{\sum_{j = 1}^{C}{w_{i}(y_{i,j}\ln\left( p_{i,j} \right)\ )}}\ $$

Where:

-   *N* is the total number of rows (observations) of your corresponding
    dataset.

-   *w* is the per row user-defined weight (defaults is 1).

-   *C* is the total number of classes (C=2 for binary classification).

-   *p* is the predicted value (uncalibrated probability) assigned to a
    given row (observation).

-   *y* is the actual target value.

**AUC (Area Under the ROC Curve)** - This model metric is used to
evaluate how well a binary classification model can distinguish between
true positives and false positives. An AUC of 1 indicates a perfect
classifier, while an AUC of .5 indicates a poor classifier, whose
performance is no better than random guessing.

H2O uses the trapezoidal rule to approximate the area under the ROC
curve. (Tip: AUC is usually not the best metric for an imbalanced binary
target because a high number of true negatives can cause the AUC to look
inflated. AUCPR or MCC is recommended for an imbalanced binary target.)

**AUCPR (Area Under the Precision-Recall Curve) -** This model metric is
used to evaluate how well a binary classification model can distinguish
between precision recall pairs or points. These values are obtained
using different thresholds on a probabilistic or other continuous-output
classifier. AUCPR is an average of the precision-recall weighted by the
probability of a given threshold.

The main difference between AUC and AUCPR is that AUC calculates the
area under the ROC curve and AUCPR calculates the area under the
Precision Recall curve. The Precision Recall curve does not care about
true negatives. For imbalanced data, a large quantity of true negatives
usually overshadows the effects of changes in other metrics like false
positives. The AUCPR will be much more sensitive to true positives,
false positives, and false negatives than AUC. As such, AUCPR is
recommended over AUC for highly imbalanced data.

{% else %}

**R2 (R Squared)** - The R2 value represents the degree that the
predicted value and the actual value move in unison. The R2 value varies
between 0 and 1 where 0 represents no correlation between the predicted
and actual value and 1 represents complete correlation.

**MSE (Mean Squared Error)** - The MSE metric measures the average of
the squares of the errors or deviations. MSE takes the distances from
the points to the regression line (these distances are the "errors") and
squaring them to remove any negative signs. MSE incorporates both the
variance and the bias of the predictor.

MSE also gives more weight to larger differences. The bigger the error,
the more it is penalized. For example, if your correct answers are 2,3,4
and the algorithm guesses 1,4,3, then the absolute error on each one is
exactly 1, so squared error is also 1, and the MSE is 1. But if the
algorithm guesses 2,3,6, then the errors are 0,0,2, the squared errors
are 0,0,4, and the MSE is a higher 1.333. The smaller the MSE, the
better the model's performance. (**Tip**: MSE is sensitive to outliers.
If you want a more robust metric, try mean absolute error (MAE).)


$$MSE =\frac{1}{N}{\sum_{i = 1}^{N}{(y_{i} - {\hat{y}}_{i}})^{2}}$$


**RMSE (Root Mean Squared Error)** - The RMSE metric evaluates how well
a model can predict a continuous value. The RMSE units are the same as
the predicted target, which is useful for understanding if the size of
the error is of concern or not. The smaller the RMSE, the better the
model's performance. (**Tip**: RMSE is sensitive to outliers. If you
want a more robust metric, try mean absolute error (MAE).)

$$RMSE=\sqrt{\frac{1}{N}{\sum_{i = 1}^{N}{(y_{i} - \widehat{y_{i}}})^{2}}}$$

Where:

-   $$N$$ is the total number of rows (observations) of your corresponding
    dataset.

-   $$y$$ is the actual target value.

-   $$\widehat{y}$$ is the predicted target value.

**RMSLE (Root Mean Squared Logarithmic Error)** - This metric measures
the ratio between actual values and predicted values and takes the log
of the predictions and actual values. Use this instead of RMSE if an
under-prediction is worse than an over-prediction. You can also use this
when you don't want to penalize large differences when both values are
large numbers.

$$RMSLE
=\sqrt{\frac{1}{N}\sum_{i = 1}^{N}{(ln(\frac{y_{i} + 1}{\widehat{y_{i}} + 1})})^{2}}$$

Where:

-   $$N$$ is the total number of rows (observations) of your corresponding
    dataset.

-   $$y$$ is the actual target value.

-   $$\widehat{y}$$ is the predicted target value.

**MAE (Mean Absolute Error)** - The mean absolute error is an average of
the absolute errors. The MAE units are the same as the predicted target,
which is useful for understanding whether the size of the error is of
concern or not. The smaller the MAE the better the model's performance.
(**Tip**: MAE is robust to outliers. If you want a metric that is
sensitive to outliers, try root mean squared error (RMSE).)

$$MAE =\frac{1}{N}\sum_{i = 1}^{N}{|y_{i} - \widehat{y_{i}}}\|$$

Where:

-   $$N$$ is the total number of rows (observations) of your corresponding
    dataset.

-   $$y$$ is the actual target value.

-   $$\widehat{y}$$ is the predicted target value.

{% endif %}