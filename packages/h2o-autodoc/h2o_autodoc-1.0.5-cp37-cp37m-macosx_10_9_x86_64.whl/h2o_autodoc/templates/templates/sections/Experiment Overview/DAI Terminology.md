Driverless AI has specific terminology that will be used throughout this document. Here we define the terms specific to model framework.

- **Features**: the columns in a tabular dataset, which represent the different characteristics collected on a given data observation.

- **Feature Tuning**: a feature engineering stage in the **Experiment Pipeline** in which features are updated using variable importance from the previous iteration as a probabilistic prior to decide what new features to create. 

- **Feature Evolution**: a feature engineering stage in the **Experiment Pipeline** in which a genetic algorithm is used to determine which feature transformations to apply.

- **Experiment**: an experiment refers to the process of specifying a prediction problem, testing out several models with different parameters and features, and finally selecting the best model, whether that be a single model or ensemble of models.

- **Experiment Pipeline**: refers to the complete data science pipeline. It starts once a dataset has been imported to Driverless AI and ends with a final model that can be exported for scoring in production. Note the experiment pipeline does not include the Machine Learning Interpretability (MLI) segment.  

- **MLI**: MLI stands for Machine Learning Interpretability and corresponds to a dashboard where the Driverless AI model developer can analyze and interpret the results of the Driverless AI final model.

- **Target**: also known as a response, dependent variable, or label, this is the column Driverless AI tries to predict.

