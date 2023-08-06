**Prevention of Over and Underfitting**

Driverless AI performs a number of checks and steps to prevent overfitting during each stage of the experiment:

- Model Evaluation
    - Each model is evaluated on hold out data, never on the training data
    - The test dataset is never used except after the final model is complete, and it is solely used to provide performance metrics on the test data to the user

- Model Training
    - Driverless AI performs early stopping for every model built, ensuring that the model will stop building when it ceases to improve on holdout data

- Feature Engineering
    - Cross validation and regularization are performed anytime a transformation requires information about the target variable
    - For example, Target Encoding always calculates the mean of the target on out-of-fold data using cross validation {% if experiment.parameters.is_timeseries %}
    - Features are never created on future data {% endif %}

Underfitting can often occur if the parameters of a model are not complex enough or the variables are not represented in the optimal way for the model type.  For example, binning a numeric variable can help prevent underfitting in linear models.  Driverless AI automatically:

- Evaluates model parameters for each algorithm selected by the user
    - In this way, Driverless AI can prevent the model from being too simple and underfitting
- Creates new features
    - In this way, Driverless AI can make sure the algorithm does not miss out on some pattern in the data because of the way the original features are defined

