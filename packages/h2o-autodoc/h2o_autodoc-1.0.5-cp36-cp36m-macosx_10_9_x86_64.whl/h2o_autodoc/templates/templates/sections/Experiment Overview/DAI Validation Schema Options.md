**Validation Scheme**
The validation scheme defines how the experiment’s dataset will be split up for model tuning and validation. Driverless AI provides three different methods for setting a validation scheme. The first two are options for independent and identically distributed data (IID) and the actual validation scheme is tied to the experimental settings (i.e., accuracy, time, and interpretability), the last option is for time dependent data, where the validation data is then split temporally. 

#### Provide a user-created validation dataset
The **Validation dataset** is used for tuning the modeling pipeline. If provided, the entire training data will be used for training, and validation of the modeling pipeline is performed with only this validation dataset. When you do not include a validation dataset, Driverless AI will do K-fold cross validation for I.I.D. experiments and multiple rolling window validation splits for time-series experiments. For this reason, it is not generally recommended to include a validation dataset as you are then validating on only a single dataset. Please note that time series experiments cannot be used with a validation dataset: including a validation dataset will disable the ability to select a time column and vice versa.

This dataset must have the same number of columns (and column types) as the training dataset. Also note that if provided, the validation set is not sampled down, so it can lead to large memory usage, even if accuracy=1 (which reduces the train size).


#### Provide a user-created fold column

If a **Fold Column** of type integer or categorical is provided, to create stratification folds during (cross-)validation, the rows with the same value in the fold column represent cohorts, and each cohort is assigned to exactly one fold. This can help to build better models when the data is grouped naturally. If left empty, the data is assumed to be IID (independent and identically distributed). For example, when viewing data to predict whether a person has pneumonia, the "person_id" column would be a good Fold Column. This is because the data may include multiple diagnostic snapshots per person, and we want to ensure that the same person’s characteristics show up only in either the training or validation frames, but not in both to avoid data leakage. Note that a Fold Column cannot be specified if a validation set is used.

#### Provide a user-created time column

If a **Time Column**, which includes a time order (timestamps for observations), is provided, it can improve model performance and model validation accuracy for problems where the target values are auto-correlated with respect to the ordering (per time-series group).

The values in this column must be a datetime format understood by *pandas.to_datetime()*, like “2017-11-29 00:30:35” or “2017/11/29”, or integer values. If *[AUTO]* is selected, all string columns are tested for potential date/datetime content and considered as potential time columns. If a time column is found, feature engineering and model validation will respect the causality of time. If [OFF] is selected, no time order is used for modeling and data may be shuffled randomly (any potential temporal causality will be ignored).

When the dataset has a date column, then in most cases, specifying *[AUTO]* for the Time Column will be sufficient. However, if a model developer selects a specific date column, then Driverless AI will provide an additional side menu. At a minimum, this side menu provides the ability to specify the number of weeks to predict and after how many weeks to start predicting; these options default to *[AUTO]*. Expert Settings are also available and can be selected to specify per-group periodicities.

