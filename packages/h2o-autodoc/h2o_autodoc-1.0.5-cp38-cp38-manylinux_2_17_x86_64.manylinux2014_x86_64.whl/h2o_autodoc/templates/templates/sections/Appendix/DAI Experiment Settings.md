This section describes the settings that are available when running an experiment in Driverless AI.

**Display Name**

Optional: Specify a display name for the new experiment. There are no character or length restrictions for naming. If this field is left blank, Driverless AI will automatically generate a name for the experiment.

**Dropped Columns**

Dropped columns are columns that you do not want to be used as predictors in the experiment. Note that Driverless AI will automatically drop ID columns and columns that contain a significant number of unique values (above `max_relative_cardinality` in the config.toml file or **Max. allowed fraction of uniques for integer and categorical cols** in Expert settings).

**Validation Dataset**

The validation dataset is used for tuning the modeling pipeline. If provided, the entire training data will be used for training, and validation of the modeling pipeline is performed with only this validation dataset. When you do not include a validation dataset, Driverless AI will do K-fold cross validation for I.I.D. experiments and multiple rolling window validation splits for time-series experiments. For this reason, it is not generally recommended to include a validation dataset as you are then validating on only a single dataset. Please note that time series experiments cannot be used with a validation dataset: including a validation dataset will disable the ability to select a time column and vice versa.

This dataset must have the same number of columns (and column types) as the training dataset. Also note that if provided, the validation set is not sampled down, so it can lead to large memory usage, even if accuracy=1 (which reduces the train size).

**Test Dataset**

The test dataset is used for testing the modeling pipeline and creating test predictions. The test set is never used during training of the modeling pipeline. (Results are the same whether a test set is provided or not.) If a test dataset is provided, then test set predictions will be available at the end of the experiment.

**Weight Column**

Optional: Column that indicates the observation weight (a.k.a. sample or row weight), if applicable. This column must be numeric with values >= 0. Rows with higher weights have higher importance. The weight affects model training through a weighted loss function and affects model scoring through weighted metrics. The weight column is not used when making test set predictions, but a weight column (if specified) is used when computing the test score.

**Fold Column**

Optional: Column to use to create stratification folds during (cross-)validation, if applicable. Must be of integer or categorical type. Rows with the same value in the fold column represent cohorts, and each cohort is assigned to exactly one fold. This can help to build better models when the data is grouped naturally. If left empty, the data is assumed to be i.i.d. (identically and independently distributed). For example, when viewing data for a pneumonia dataset, person_id would be a good Fold Column. This is because the data may include multiple diagnostic snapshots per person, and we want to ensure that the same person’s characteristics show up only in either the training or validation frames, but not in both to avoid data leakage. Note that a fold column cannot be specified if a validation set is used or if a Time Column is specified.

**Time Column**

Optional: Specify a column that provides a time order (time stamps for observations), if applicable. This can improve model performance and model validation accuracy for problems where the target values are auto-correlated with respect to the ordering (per time-series group).

The values in this column must be a datetime format understood by pandas.to_datetime(), like “2017-11-29 00:30:35” or “2017/11/29”, or integer values. If [AUTO] is selected, all string columns are tested for potential date/datetime content and considered as potential time columns. If a time column is found, feature engineering and model validation will respect the causality of time. If [OFF] is selected, no time order is used for modeling and data may be shuffled randomly (any potential temporal causality will be ignored).

When your data has a date column, then in most cases, specifying [AUTO] for the Time Column will be sufficient. However, if you select a specific date column, then Driverless AI will provide you with an additional side menu. From this side menu, you can specify Time Group columns or specify [Auto] to let Driverless AI determine the best time group columns. You can also specify the Forecaset Horizon in weeks and the Gap between the train and test periods.

**Notes**:

- Engineered features will be used for MLI when a time series experiment is built. This is because munged time series features are more useful features for MLI compared to raw time series features.

- A Time Column cannot be specified if a Fold Column is specified. This is because both fold and time columns are only used to split training datasets into training/validation, so once you split by time, you cannot also split with the fold column. If a Time Column is specified, then the time group columns play the role of the fold column for time series.

- A Time Column cannot be specified if a validation dataset is used.

- Accuracy, Time, and Interpretability Knobs.

- The experiment preview describes what the Accuracy, Time, and Interpretability settings mean for your specific experiment. This preview will automatically update if any of the knob values change. The following is more detailed information describing how these values affect an experiment.

**Accuracy**

As accuracy increases (as indicated by the tournament\_* toml settings), Driverless AI gradually adjusts the method for performing the evolution and ensemble. At low accuracy, Driverless AI varies features and models, but they all compete evenly against each other. At higher accuracy, each independent main model will evolve independently and be part of the final ensemble as an ensemble over different main models. At higher accuracies, Driverless AI will evolve+ensemble feature types like Target Encoding on and off that evolve independently. Finally, at highest accuracies, Driverless AI performs both model and feature tracking and ensembles all those variations.
The following table describes how the Accuracy value affects a Driverless AI experiment.

{{section.table(
    columns=['Accuracy', 'Max Rows x Cols', 'Ensemble Level', 'Target Transformation', 'Parameter Tuning Level', 'Num Individuals', 'Num Folds', 'Only First Fold Model', 'Distribution Check'],
    data=[
        ['1', '100K', '0', 'False', '0', 'Auto', '3', 'True', 'No'],
        ['2', '1M', '0', 'False', '0', 'Auto', '3', 'True', 'No'],
        ['3', '50M', '0', 'True', '1', 'Auto', '3', 'True', 'No'],
        ['4', '100M', '0', 'True', '1', 'Auto', '3-4', 'True', 'No'],
        ['5', '200M', '1', 'True', '1', 'Auto', '3-4', 'True', 'Yes'],
        ['6', '500M', '2', 'True', '1', 'Auto', '3-5', 'True', 'Yes'],
        ['7', '750M', '<=3', 'True', '2', 'Auto', '3-10', 'Auto', 'Yes'],
        ['8', '1B', '<=3', 'True', '2', 'Auto', '4-10', 'Auto', 'Yes'],
        ['9', '2B', '<=3', 'True', '3', 'Auto', '4-10', 'Auto', 'Yes'],
        ['10', '10B', '<=4', 'True', '3', 'Auto', '4-10', 'Auto', 'Yes']
    ]
)}}

**Note**: A check for a shift in the distribution between train and test is done for accuracy >= 5.
The list below includes more information about the parameters that are used when calculating accuracy.

- **Max Rows x Cols**: The maximum number of rows x columns to use in model training
	- For classification, stratified random row sampling is performed (by target)
	- For regression, random row sampling is performed

- **Ensemble Level**: The level of ensembling done for the final model (if no time column is selected)
	- 0: single model
	- 1: 1x 4-fold models ensembled together
 	- 2: 2x 5-fold models ensembled together
 	- 3: 5x 5-fold models ensembled together
 	- 4: 8x 5-fold models ensembled together
 	- If ensemble level > 0, then the final model score shows an error estimate that includes the data generalization error (standard deviation of scores over folds) and the error in the estimate of the score (bootstrap score’s standard deviation with sample size same as data size).
	- For accuracy >= 8, the estimate of the error in the validation score reduces, and the error in the score is dominated by the data generalization error.
	- The estimate of the error in the test score is estimated by the maximum of the bootstrap with sample size equal to the test set size and the validation score’s error.
- **Target Transformation**: Try target transformations and choose the transformation(s) that have the best score(s).

Possible transformations: identity, unit_box, log, square, square root, double square root, inverse, Anscombe, logit, sigmoid

- **Parameter Tuning Level**: The level of parameter tuning done
	- 0: no parameter tuning
	- 1: 8 different parameter settings
	- 2: 16 different parameter settings
	- 3: 32 different parameter settings
	- 4: 64 different parameter settings
	- Optimal model parameters are chosen based on a combination of the model’s accuracy, training speed, and complexity.

- **Num Individuals**: The number of individuals in the population for the genetic algorithms
	- Each individual is a gene. The more genes, the more combinations of features are tried.
	- The number of individuals is automatically determined and can depend on the number of GPUs. Typical values are between 4 and 16.

- **Num Folds**: The number of internal validation splits done for each pipeline
	- If the problem is a classification problem, then stratified folds are created.

- **Only First Fold Model**: Whether to only use the first fold split for internal validation to save time
	- Example: Setting Num Folds to 3 and Only First Fold Model = True means you are splitting the data into 67% training and 33% validation.
	- If “Only First Fold Model” is False, then errors on the score shown during feature engineering include the data generalization error (standard deviation of scores over folds) and the error in the estimate of the score (bootstrap score’s standard deviation with a sample size the same as the data size).
	- If “Only First Fold Model” is True, then errors on the score shown during feature engineering include only the error in the estimate of the score (bootstrap score’s standard deviation with a sample size same as the data size).
	- For accuracy >= 8, the estimate of the error in the score reduces, and the error in the score is dominated by the data generalization error. This provides the most accurate generalization error.

- **Early Stopping Rounds**: Time-based means based upon the Time table below.

- **Distribution Check**: Checks whether validation or test data are drawn from the same distribution as the training data. Note that this is purely informative to the user. Driverless AI does not take information from the test set into consideration during training.

- **Strategy**: Feature selection strategy (to prune-away features that do not clearly give improvement to model score). Feature selection is triggered by interpretability. Strategy = “FS” if interpretability >= 6; otherwise strategy is None.

**Time**

This specifies the relative time for completing the experiment (i.e., higher settings take longer). Early stopping will take place if the experiment doesn’t improve the score for the specified amount of iterations.

{{section.table(
    columns=['Time', 'Iterations', 'Early Stopping Rounds'],
    data=[
        ['1', '1-5', 'None'],
        ['2', '10', '5'],
        ['3', '30', '5'],
        ['4', '40', '5'],
        ['5', '50', '10'],
        ['6', '100', '10'],
        ['7', '150', '15'],
        ['8', '200', '20'],
        ['9', '300', '30'],
        ['10', '500', '50']
    ]
)}}

**Note**: See the Accuracy table for cases when not based upon time.

**Interpretability**

In the following tables, **Ensemble Level** is the level of ensembling done for the final model (if no time column is selected).

- 0: single model

- 1: 1x 4-fold models ensembled together

- 2: 2x 5-fold models ensembled together

- 3: 5x 5-fold models ensembled together

If **Monotonicity Constraints** are enabled, the model will satisfy knowledge about monotonicity in the data and monotone relationships between the predictors and the target variable. For example, in house price prediction, the house price should increase with lot size and number of rooms, and should decrease with crime rate in the area. If enabled, Driverless AI will automatically determine if monotonicity is present and enforce it in its modeling pipelines. Depending on the correlation, Driverless AI will assign positive, negative, or no monotonicity constraints. Monotonicity is enforced if the absolute correlation is greater than 0.1. All other predictors will not have monotonicity enforced.

{{section.table(
    columns=['Interpretability', 'Ensemble Level', 'Monotonicity Constraints'],
    data=[
        ['<= 5', '<= 3', 'Disabled'],
        ['>= 6', '<= 2', 'Disabled'],
        ['>= 7', '<= 2', 'Enabled'],
        ['>= 8', '<= 1', 'Enabled'],
        ['10', '0', 'Enabled']
    ]
)}}


{{section.table(
    columns=['Interpretability', 'Transformers**'],
    data=[
        ['<= 5', 'All'],
        ['0-5', 'Interpretability#5 - [TruncSvdNum, ClusterDist]'],
        ['0-6', 'Interpretability#6 - [ClusterTE, ClusterID, IsolationForestAnomaly]'],
        ['0-7', 'Interpretability#7 - [NumToCatTE]'],
        ['0-8', 'Interpretability#8 - [NumCatTE, NumToCatWoE]'],
        ['0-9', 'Interpretability#9 - [BulkInteractions, WeightOfEvidence, CvCatNumEncode, NumToCatWeightOfEvidenceMonotonic]'],
        ['0-10', 'Interpretability#10 - [CVTargetEncodeFit, CVCatNumericEncodeF, Frequent]']
    ]
)}}

** Interpretability# - [lost transformers] explains which transformers are lost by going up by 1 to that interpretability.

** Exception - NumToCatWeightOfEvidenceMonotonic removed for interpretability<=6.

** For interpretability <= 10, i.e. only [Filter for numeric, Frequent for categorical, DateTime for Date+Time, Date for dates, and Text for text]

- **Target Transformers**:
	- For regression, applied on target before any other transformations.

{{section.table(
    columns=['Interpretability', 'Target Transformer'],
    data=[
        ['<=10', 'TargetTransformer_identity'],
        ['<=10', 'TargetTransformer_unit_box'],
        ['<=10', 'TargetTransformer_log'],
        ['<= 9', 'TargetTransformer_square'],
        ['<= 9', 'TargetTransformer_sqrt'],
        ['<= 8', 'TargetTransformer_double_sqrt'],
        ['<= 6', 'TargetTransformer_logit'],
        ['<= 6', 'TargetTransformer_sigmoid'],
        ['<= 5', 'TargetTransformer_Anscombe'],
        ['<= 4', 'TargetTransformer_inverse']
    ]
)}}

- **Date Types Detected**:
	- categorical
	- date
	- datetime
	- numeric
	- text
 
- **Transformers used on raw features to generate new features**:

{{section.table(
    columns=['Interpretability', 'Transformer'],
    data=[
        ['<=10', 'Filter'],
        ['<=10', 'DateTime'],
        ['<=10', 'Date'],
        ['<=10', 'Text'],
        ['<=10', 'TextLin'],
        ['<=10', 'CvTargetEncodeMulti'],
        ['<=10', 'CvTargetEncodeSingle'],
        ['<=9', 'CvCatNumEncode'],
        ['<=9', 'WeightOfEvidence'],
        ['<=9 and >=7', 'NumToCatWeightOfEvidenceMonotonic'],
        ['<=9', 'BulkInteractions'],
        ['<=8', 'NumToCatWeightOfEvidence'],
        ['<=8', 'NumCatTargetEncodeMulti'],
        ['<=8', 'NumCatTargetEncodeSingle'],
        ['<=7', 'Frequent'],
        ['<=7', 'NumToCatTargetEncodeMulti'],
        ['<=7', 'NumToCatTargetEncodeSingle'],
        ['<=6', 'ClusterIDTargetEncodeMulti'],
        ['<=6', 'ClusterIDTargetEncodeSingle'],
        ['<=5', 'TruncSvdNum'],
        ['<=5', 'ClusterDist']
    ]
)}}

- ** **Default N-way interactions are up to 8-way except**:
	- BulkInteractions are always 2-way.
	- Interactions are minimal-way (e.g. 1-way for CvTargetEncode) if interpretability=10.

- **Feature importance threshold below which features are removed**

{{section.table(
    columns=['Interpretability', 'Threshold'],
    data=[
        ['10', 'config.toml varimp_threshold_at_interpretability_10'],
        ['9', 'varimp_threshold_at_interpretability_10/5.0'],
        ['8', 'varimp_threshold_at_interpretability_10/7.0'],
        ['7', 'varimp_threshold_at_interpretability_10/10.0'],
        ['6', 'varimp_threshold_at_interpretability_10/20.0'],
        ['5', 'varimp_threshold_at_interpretability_10/30.0'],
        ['4', 'varimp_threshold_at_interpretability_10/50.0'],
        ['3', 'varimp_threshold_at_interpretability_10/500.0'],
        ['2', 'varimp_threshold_at_interpretability_10/5000.0'],
        ['1', '1E-30']
    ]
)}}

** Also used for strategy=FS dropping of features, but the threshold is the above value multiplied by config.varimp_fspermute_factor.

- **Base model used for scoring features and building final model**

{{section.table(
    columns=['Interpretability', 'Allowed Base Model'],
    data=[
        ['10', 'Only GLM if glm_enable_more==True or glm_enable_exlcusive=True, GBM+GLM if glm_enable==True, else only GBM'],
        ['9', 'GBM unless glm_enable_exlcusive=True, GBM+GLM if glm_enable_more==True'],
        ['8', 'GBM unless glm_enable_exlcusive=True, GBM+GLM if glm_enable_more==True'],
        ['7', 'GBM unless glm_enable_exlcusive=True, GBM+GLM if glm_enable_more==True'],
        ['6', 'GBM unless glm_enable_exlcusive=True, GBM+GLM if glm_enable_more==True'],
        ['5', 'GBM unless glm_enable_exlcusive=True'],
        ['4', 'GBM unless glm_enable_exlcusive=True'],
        ['3', 'GBM unless glm_enable_exlcusive=True'],
        ['2', 'GBM unless glm_enable_exlcusive=True'],
        ['1', 'GBM unless glm_enable_exlcusive=True']
    ]
)}}

** When mixing GBM and GLM in parameter tuning, the search space is split 50%/50% between GBM and GLM.

Classification, Reproducible, and Enable GPUs Buttons

- **Classification** or **Regression** button. Driverless AI automatically determines the problem type based on the response column. Though not recommended, you can override this setting by clicking this button.

- **Reproducible**: This button allows you to build an experiment with a random seed and get reproducible results. If this is disabled (default), then results will vary between runs.
- **Enable GPUs**: Specify whether to enable GPUs. (Note that this option is ignored on CPU-only systems.)

**Expert Settings**

This section describes the Expert Settings options that are available when starting an experiment. Note that the default values for these options are derived from the environment variables in the config.toml file.

Note that by default the feature brain pulls in any better model regardless of the features even if the new model disabled those features. For full control over features pulled in via changes in these Expert Settings, users should set the **Feature Brain Level** option to 0.

**Experiment Settings**

Max Runtime in Minutes Before Triggering the Finish Button
Specify the maximum runtime in minutes for an experiment. This is equivalent to pushing the **Finish** button once half of the specified time value has elapsed. Note that the overall enforced runtime is only an approximation.

This value defaults to 1440, which is the equivalent of a 24 hour approximate overall runtime. The **Finish** button will be automatically selected once 12 hours have elapsed, and Driverless AI will subsequently attempt to complete the overall experiment in the remaining 12 hours. Set this value to 0 to disable this setting.

**Pipeline Building Recipe**

Specify the Pipeline Building recipe type. **Auto** (default) specifies that all models and features are automatically determined by experiment settings, config.toml settings, and the feature engineering effort. **Compliant** is similar to **Auto** except for the following:

- Interpretability is forced to be 10.

- Only use GLM or RuleFit.

- Treat some numerical features as categorical. For instance, sometimes an integer column may not represent a numerical feature but represents different numerical codes instead.

- Doesn’t use any ensemble.

- No feature brain is used.

- Interaction depth is set to 1.

- Target transformer is forced to be identity for regression.

- Doesn’t use distribution shift between train, valid, and test to drop features.

**Min Number of Rows Needed to Run an Experiment**

Specify the minimum number of rows that a dataset must contain in order to run an experiment. This value defaults to 100.

**Reproducibility Level**

Specify one of the following levels of reproducibility (note that this setting is only active while reproducible mode is enabled):

- 1 = Same experiment results for same O/S, same CPU(s), and same GPU(s) (Default)

- 2 = Same experiment results for same O/S, same CPU architecture, and same GPU architecture

- 3 = Same experiment results for same O/S, same CPU archicture (excludes GPUs)

- 4 = Same experiment results for same O/S (best approximation)

This value defaults to 1.

**Random Seed**

Specify a random seed for the experiment. When a seed is defined and the reproducible button is enabled (not by default), the algorithm will behave deterministically.

**Allow Different Sets of Classes Across All Train/Validation Fold Splits**

(**Note**: Applicable for multiclass problems only.) Specify whether to enable full cross-validation (multiple folds) during feature evolution as opposed to a single holdout split. This is enabled by default.

**Max Number of Classes for Classification Problems**

Specify the maximum number of classes to allow for a classification problem. A higher number of classes may make certain processes more time-consuming. Memory requirements also increase with a higher number of classes. This value defaults to 200.

**Model/Feature Brain Level**

Specify whether to use H2O.ai brain, which enables local caching and smart re-use (checkpointing) of prior experiments to generate useful features and models for new experiments. It can also be used to control checkpointing for experiments that have been paused or interrupted.
When enabled, this will use the H2O.ai brain cache if the cache file:

- has any matching column names and types for a similar experiment type

- has classes that match exactly

- has class labels that match exactly

- has basic time series choices that match

- the interpretability of the cache is equal or lower

- the main model (booster) is allowed by the new experiment

- -1: Don’t use any brain cache (default)

- 0: Don’t use any brain cache but still write to cache. Use case: Want to save the model for later use, but we want the current model to be built without any brain models.

- 1: Smart checkpoint from the latest best individual model. Use case: Want to use the latest matching model. The match may not be precise, so use with caution.

- 2: Smart checkpoint if the experiment matches all column names, column types, classes, class labels, and time series options identically. Use case: Driverless AI scans through the H2O.ai brain cache for the best models to restart from.

- 3: Smart checkpoint like level #1, but for the entire population. Tune only if the brain population is of insufficient size. Note that this will re-score the entire population in a single iteration, so it appears to take longer to complete first iteration.

- 4: Smart checkpoint like level #2, but for the entire population. Tune only if the brain population is of insufficient size. Note that this will re-score the entire population in a single iteration, so it appears to take longer to complete first iteration.

- 5: Smart checkpoint like level #4, but will scan over the entire brain cache of populations to get the best scored individuals. Note that this can be slower due to brain cache scanning if the cache is large.

When enabled, the directory where the H2O.ai Brain meta model files are stored is H2O.ai_brain. In addition, the default maximum brain size is 20GB. Both the directory and the maximum size can be changed in the config.toml file. This value defaults to 2.

**Feature Brain Save Every Which Iteration**

Save feature brain iterations every iter_num % feature_brain_iterations_save_every_iteration == 0, to be able to restart/refit with which_iteration_brain >= 0. This is disabled (0) by default.

- -1: Don’t use any brain cache.

- 0: Don’t use any brain cache but still write to cache.

- 1: Smart checkpoint if an old experiment_id is passed in (for example, via running “resume one like this” in the GUI).

- 2: Smart checkpoint if the experiment matches all column names, column types, classes, class labels, and time series options identically. (default)

- 3: Smart checkpoint like level #1, but for the entire population. Tune only if the brain population is of insufficient size.

- 4: Smart checkpoint like level #2, but for the entire population. Tune only if the brain population is of insufficient size.

- 5: Smart checkpoint like level #4, but will scan over the entire brain cache of populations (starting from resumed experiment if chosen) in order to get the best scored individuals.

When enabled, the directory where the H2O.ai Brain meta model files are stored is H2O.ai_brain. In addition, the default maximum brain size is 20GB. Both the directory and the maximum size can be changed in the config.toml file.

**Feature Brain Restart from Which Iteration**

When performing restart or re-fit of type feature_brain_level with a resumed ID, specify which iteration to start from instead of only last best. Available options include:

- -1: Use the last best

- 1: Run one experiment with feature_brain_iterations_save_every_iteration=1 or some other number

- 2: Identify which iteration brain dump you wants to restart/refit from

- 3: Restart/Refit from the original experiment, setting which_iteration_brain to that number here in expert settings.

**Note**: If restarting from a tuning iteration, this will pull in the entire scored tuning population and use that for feature evolution. This value defaults to -1.

Feature Brain Adds Features with New Columns Even During Retraining of Final Model

Specify whether to add additional features from new columns to the pipeline, even when performing a retrain of the final model. Use this option if you want to keep the same pipeline regardless of new columns from a new dataset. New data may lead to new dropped features due to shift or leak detection. Disable this to avoid adding any columns as new features so that the pipeline is perfectly preserved when changing data. This is enabled by default.

**Min DAI Iterations**

Specify the minimum number of Driverless AI iterations for an experiment. This can be used during restarting, when you want to continue for longer despite a score not improving. This value defaults to 0.

**Select Target Transformation of the Target for Regression Problems**

Specify whether to automatically select target transformation for regression problems. Selecting **Identity** disables any transformation. This is set to **Auto** by default.

Tournament Model for Genetic Algorithm
Select a method to decide which models are best at each iteration. This is set to Auto by default. Choose from the following:

- **Auto**: Choose based on scoring metric

- **Fullstack**: Choose from optimal model and feature types

- **Feature**: Individuals with similar feature types compete

- **Model**: Individuals with same model type compete

- **Uniform**: All individuals in population compete

**Enable Extra Logging for Ensemble Meta Learner**

Specify whether to enable extra logging for an ensemble meta learner. This is enabled by default.

**Number of Cross-Validation Folds or Maximum Time-Based Splits for Feature Evolution**

Specify a fixed number of folds (if >= 2) for cross-validation or the maximum allowed time-based splits (if >= 1) for time series experiments. Note that the actual number of splits allowed can be less and is determined at experiment run-time. This value defaults to 0.

**Number of Cross-Validation Folds or Maximum Time-Based Splits for Final Model**

Specify a fixed number of folds (if >= 2) for cross-validation or maximum allowed time-based splits (if >= 1) for time series. Note that the actual number of allowed splits can be smaller, and that the number of allowed splits is determined at the time an experiment is run. This value defaults to 0.

**Maximum Number of Fold IDs to Show in Logs**

Specify the maximum number of fold IDs to show in an experiment’s logs. This value defaults to 10.

**Max Number of Rows Times Number of Columns for Feature Evolution Data Splits**

Specify the maximum number of rows allowed for feature evolution data splits (not for the final pipeline). This value defaults to 100,000,000.

**Max Number of Rows Times Number of Columns for Reducing Training Dataset**

Specify the upper limit on the number of rows times the number of columns for training the final pipeline. This value defaults to 500,000,000.

**Maximum Size of Validation Data Relative to Training Data**

Specify the maximum size of the validation data relative to the training data. Smaller values can make the final pipeline model training process quicker. Note that final model predictions and scores will always be provided on the full dataset provided. This value defaults to 2.0.

**Model Settings**

**XGBoost GBM Models**

This option allows you to specify whether to build XGBoost models as part of the experiment (for both the feature engineering part and the final model). XGBoost is a type of gradient boosting method that has been widely successful in recent years due to its good regularization techniques and high accuracy.

**XGBoost Dart Models**

This option specifies whether to use XGBoost’s Dart method when building models for experiment (for both the feature engineering part and the final model).

**GLM Models**

This option allows you to specify whether to build GLM models (generalized linear models) as part of the experiment (usually only for the final model unless it’s used exclusively). GLMs are very interpretable models with one coefficient per feature, an intercept term and a link function.

**LightGBM Models**

This option allows you to specify whether to build LightGBM models as part of the experiment. LightGBM Models are the default models.

**TensorFlow Models**

This option allows you to specify whether to build TensorFlow models as part of the experiment (usually only for text features engineering and for the final model unless it’s used exclusively). Enable this option for NLP experiments.

**FTRL Models**

This option allows you to specify whether to build Follow the Regularized Leader (FTRL) models as part of the experiment. Note that MOJOs are not yet supported (only Python scoring pipelines). FTRL supports binomial and multinomial classification for categorical targets, as well as regression for continuous targets.

**RuleFit Models**

This option allows you to specify whether to build RuleFit models as part of the experiment. Note that MOJOs are not yet supported (only Python scoring pipelines). Note that multiclass classification is not yet supported for RuleFit models. Rules are stored to text files in the experiment directory for now.

**LightGBM Boosting Types**

Specify which boosting types to enable for LightGBM. Select one or more of the following:

- **gbdt**: Boosted trees

- **rf**: Random Forest

- **dart**: Dropout boosted trees with no early stopping

**gbdt** and **rf** are both enabled by default.

**LightGBM Categorical Support**

Specify whether to enable LightGBM categorical feature support (currently only available for CPU mode). This is enabled by default.

**Max Number of Trees/Iterations**

Specify the upper limit on the number of trees (GBM) or iterations (GLM). This defaults to 3000. Depending on accuracy settings, a fraction of this limit will be used.

**Minimum Learning Rate for Final Ensemble GBM Models**

Specify the minimum learning rate for final ensemble GBM models. This value defaults to 0.01.

**Maximum Learning Rate for Final Ensemble GBM Models**

Specify the maximum learning rate for final ensemble GBM models. This value defaults to 0.05.

**Reduction Factor for Number of Trees/Iterations During Feature Evolution**

Specify the factor by which max_nestimators is reduced for tuning and feature evolution. This option defaults to 0.2. So by default, Driverless AI will produce no more than 0.2 * 3000 trees/iterations during feature evolution.

**Minimum Learning Rate for Feature Engineering GBM Models**

Specify the minimum learning rate for feature engineering GBM models. This value defaults to 0.05.

**Max Learning Rate for Tree Models**

Specify the maximum learning rate for tree models during feature engineering. Larger values can speed up feature engineering, but can hurt accuracy. This value defaults to 0.5.

**Max Number of Epochs for TensorFlow/FTRL**

When building TensorFlow or FTRL models, specify the maximum number of epochs to train models with (it might stop earlier). This value defaults to 10. This option is ignored if **TensorFlow models** and/or **FTRL models** is disabled.

**Max Number of Rules for RuleFit**
Specify the maximum number of rules to be used for RuleFit models. This defaults to -1, which specifies to use all rules.

**Ensemble Level for Final Modeling Pipeline**

Specify one of the following ensemble levels:

- -1 = auto, based upon ensemble_accuracy_switch, accuracy, size of data, etc. (Default)

- 0 = No ensemble, only final single model on validated iteration/tree count. Note that holdout predicted probabilities will not be available.

- 1 = 1 model, multiple ensemble folds (cross-validation)

- 2 = 2 models, multiple ensemble folds (cross-validation)

- 3 = 3 models, multiple ensemble folds (cross-validation)

- 4 = 4 models, multiple ensemble folds (cross-validation)

**Number of Models During Tuning Phase**

Specify the number of models to tune during pre-evolution phase. Specify a lower value to avoid excessive tuning, or specify a higher to perform enhanced tuning. This option defaults to -1 (auto).

**Sampling Method for Imbalanced Binary Classification Problems**

Specify the sampling method for imbalanced binary classification problems. This is set to off by default. Choose from the following options:

- **auto**: sample both classes as needed, depending on data

- **over_under_sampling**: over-sample the minority class and under-sample the majority class, depending on data

- **under_sampling**: under-sample the majority class to reach class balance

- **off**: do not perform any sampling

**Ratio of Majority to Minority Class for Imbalanced Binary Classification to Trigger Special Sampling Techniques (if Enabled)**

For imbalanced binary classification problems, specify the ratio of majority to minority class. Special imbalanced models with sampling techniques are enabled when the ratio is equal to or greater than the specified ratio. This value defaults to 5.

**Ratio of Majority to Minority Class for Heavily Imbalanced Binary Classification to Only Enable Special Sampling Techniques if Enabled**

For heavily imbalanced binary classification, specify the ratio of the majority to minority class equal and above which to enable only special imbalanced models on the full original data without upfront sampling. This value defaults to 25.

**Number of Bags for Sampling Methods for Imbalanced Binary Classification (if Enabled)**

Specify the number of bags for sampling methods for imbalanced binary classification. This value defaults to -1.

**Hard Limit on Number of Bags for Sampling Methods for Imbalanced Binary Classification During Feature Evolution Phase**

Specify the limit on the number of bags for sampling methods for imbalanced binary classification (not used for final models). This value defaults to 3.

**Max Size of Data Sampled During Imbalanced Sampling**

Specify the maximum size of the data sampled during imbalanced sampling in terms of the dataset’s size. This setting controls the approximate number of bags and is only active when the “Hard limit on number of bags for sampling methods for imbalanced binary classification during feature evolution phase” option is set to -1. This value defaults to 1.

**Target Fraction of Minority Class After Applying Under/Over-Sampling Techniques**

Specify the target fraction of a minority class after applying under/over-sampling techniques. A value of 0.5 means that models/algorithms will be given a balanced target class distribution. When starting from an extremely imbalanced original target, it can be advantageous to specify a smaller value such as 0.1 or 0.01. This value defaults to -1.

**Max Number of Automatic FTRL Interactions Terms for 2nd, 3rd, 4th order interactions terms (Each)**

Specify a limit for the number of FTRL interactions terms sampled for each of second, third, and fourth order terms. This value defaults to 10,000.

**Enable Detailed Scored Model Info**

Specify whether to dump every scored individual’s model parameters to a csv/tabulated file. If enabled (default), Driverless AI produces files such as “individual_scored_id%d.iter%d*params*”. This is enabled by default.

**For Classification Problems with This Many Classes, Default to TensorFlow**

Specify the number of classes above which to use TensorFlow when it is enabled. Others model that are set to **auto** will not be used above this number (models set to on, however, are still used). This value defaults to 10.

**Features Settings**

**Feature Engineering Effort**

Specify a value from 0 to 10 for the Driverless AI feature engineering effort. Higher values generally lead to more time (and memory) spent in feature engineering. This value defaults to 5.

- 0: Keep only numeric features. Only model tuning during evolution.

- 1: Keep only numeric features and frequency-encoded categoricals. Only model tuning during evolution.

- 2: Similar to 1 but instead just no Text features. Some feature tuning before evolution.

- 3: Similar to 5 but only tuning during evolution. Mixed tuning of features and model parameters.

- 4: Similar to 5, but slightly more focused on model tuning.

- 5: Balanced feature-model tuning. (Default)

- 6-7: Similar to 5 but slightly more focused on feature engineering.

- 8: Similar to 6-7 but even more focused on feature engineering with high feature generation rate and no feature dropping even if high interpretability.

- 9-10: Similar to 8 but no model tuning during feature evolution.

**Data Distribution Shift Detection**

Specify whether Driverless AI should detect data distribution shifts between train/valid/test datasets (if provided). Currently, this information is only presented to the user and not acted upon.

**Data Distribution Shift Detection Drop of Features**

Specify whether to drop high-shift features. This defaults to Auto. Note that Auto for time series experiments turns this feature off.

**Max Allowed Feature Shift (AUC) Before Dropping Feature**

Specify the maximum allowed AUC value for a feature before dropping the feature.

When train and test differ (or train/valid or valid/test) in terms of distribution of data, then there can be a model built that tells you for each row whether the row is in train or test. That model includes an AUC value. If the AUC is above this specified threshold, then Driverless AI will consider it a strong enough shift to drop features that are shifted.

This value defaults to 0.999.

**Leakage Detection**

Specify whether to check leakage for each feature. Note that this is always disabled if a fold column is specified and if the experiment is a time series experiment. This is set to **AUTO** by default.

**Leakage Detection Dropping AUC/R2 Threshold**

If Leakage Detection is enabled, specify to drop features for which the AUC (classification)/R2 (regression) is above this value. This value defaults to 0.999.

**Max Rows Times Columns for Leakage**

Specify the maximum number of rows times the number of columns to trigger sampling for leakage checks. This value defaults to 10,000,000.

**Report Permutation Importance on Original Features**

Specify whether Driverless AI reports permutation importance on original features. This is disabled by default.

**Maximum Number of Rows to Perform Permutation-Based Feature Selection**

Specify the maximum number of rows to when performing permutation feature importance. This value defaults to 1,000,000.

**Max Number of Original Features Used**

Specify the maximum number of features you want to be selected in an experiment. This value defaults to 10,000.

**Max Number of Original Non-Numeric Features**

Specify the number of non-numeric columns to be selected. Feature selection is performed on all features when this value is exceeded. This value defaults to 300.

**Max Number of Original Features Used for FS Individual**

Specify the maximum number of features you want to be selected in an experiment. Additional columns above the specified value add special individual with original columns reduced. This value defaults to 500.

**Number of Original Numeric Features to Trigger Feature Selection Model Type**

The maximum number of original numeric columns, above which Driverless AI will do feature selection. Note that this is applicable only to special individuals with original columns reduced. A separate individual in the genetic algorithm is created by doing feature selection by permutation importance on original features. This value defaults to 500.

**Number of Original Non-Numeric Features to Trigger Feature Selection Model Type**

The maximum number of original non-numeric columns, above which Driverless AI will do feature selection. Note that this is applicable only to special individuals with original columns reduced. A separate individual in the genetic algorithm is created by doing feature selection by permutation importance on original features. This value defaults to 200.

**Max Allowed Fraction of Uniques for Integer and Categorical Columns**

Specify the maximum fraction of unique values for integer and categorical columns. If the column has a larger fraction of unique values than that, it will be considered an ID column and ignored. This value defaults to 0.95.

**Max Number of Unique Values for Int/Float to be Categoricals**

Specify the number of unique values for integer or real columns to be treated as categoricals. This value defaults to 50.

**Max Number of Engineered Features**

Specify the maximum number of features to include in the final model’s feature engineering pipeline. If -1 is specified (default), then Driverless AI will automatically determine the number of features.

**Correlation Beyond Which Triggers Monotonicity Constraints (if Enabled)**

Specify the threshold of Pearson product-moment correlation coefficient between numerical and encoded transformed feature and target. This value defaults to 0.1.

**Max Feature Interaction Depth**

Specify the maximum number of features to be used for interaction features like grouping for target encoding, weight of evidence and other likelihood estimates.

Exploring feature interactions can be important in gaining better predictive performance. The interaction can take multiple forms (i.e. feature1 + feature2 or feature1 * feature2 + … featureN). Although certain machine learning algorithms (like tree-based methods) can do well in capturing these interactions as part of their training process, still generating them may help them (or other algorithms) yield better performance.

The depth of the interaction level (as in “up to” how many features may be combined at once to create one single feature) can be specified to control the complexity of the feature engineering process. Higher values might be able to make more predictive models at the expense of time. This value defaults to 8.

**Enable Target Encoding**

Specify whether to use Target Encoding when building the model. Target encoding refers to several different feature transformations (primarily focused on categorical data) that aim to represent the feature using information of the actual target variable. A simple example can be to use the mean of the target to replace each unique category of a categorical feature. These types of features can be very predictive but are prone to overfitting and require more memory as they need to store mappings of the unique categories and the target values.

**Enable Lexicographical Label Encoding**

Specify whether to enable lexicographical label encoding. This is disabled by default.

**Enable Isolation Forest Anomaly Score Encoding**

Specify whether to enable Isolation Forest anomaly score encoding. This is disabled by default.

**Enable One HotEncoding**

Specify whether one-hot encoding is enabled. The default Auto setting is only applicable for small datasets and GLMs.

**Number of Estimators for Isolation Forest Encoding**

Specify the number of estimators for Isolation Forest encoding. This value defaults to 200.

**Drop Constant Columns**

Specify whether to drop columns with constant values. This is enabled by default.

**Drop ID Columns**

Specify whether to drop columns that appear to be an ID. This is enabled by default.

**Don’t Drop Any Columns**

Specify whether to avoid dropping any columns (original or derived). This is disabled by default.

**Features to Drop**

Specify which features to drop. This setting allows you to select many features at once by copying and pasting a list of column names (in quotes) separated by commas.

**Enable Detailed Scored Features Info**

Specify whether to dump every scored individual’s variable importance (both derived and original) to a csv/tabulated/json file. If enabled, Driverless AI produces files such as “individual_scored_id%d.iter%d*features*”. This is disabled by default.

**Enable Detailed Logs for Timing and Types of Features Produced**

Specify whether to dump every scored fold’s timing and feature info to a timings.txt file. This is disabled by default.

**Time Series Settings**

**Time Series Lag-Based Recipe**

This recipe specifies whether to include Time Series lag features when training a model with a provided (or autodetected) time column. Lag features are the primary automatically generated time series features and represent a variable’s past values. At a given sample with time stamp tt, features at some time difference TT (lag) in the past are considered. For example if the sales today are 300, and sales of yesterday are 250, then the lag of one day for sales is 250. Lags can be created on any feature as well as on the target. Lagging variables are important in time series because knowing what happened in different time periods in the past can greatly facilitate predictions for the future. 

**Generate Holiday Features**

For time-series experiments, specify whether to generate holiday features for the experiment. This is enabled by default.

**Time-Series Lags Override**

Specify the override lags to be used. These can be used to give more importance to the lags that are still considered after the override is applied. The following examples show the variety of different methods that can be used to specify override lags:

- “[7, 14, 21]” specifies this exact list

- “21” specifies every value from 1 to 21

- “21:3” specifies every value from 1 to 21 in steps of 3

- “5-21” specifies every value from 5 to 21

- “5-21:3” specifies every value from 5 to 21 in steps of 3

**Smallest Considered Lag Size**

Specify a minimum considered lag size. This value defaults to -1.

**Enable Feature Engineering from Time Column**

Specify whether to enable feature engineering based on the selected time column, e.g. Date~weekday. This is enabled by default.

**Enable Feature Engineering from Integer Time Column**

Specify whether to enable feature engineering from an integer time column. Note that if you are using a time series recipe, using a time column (numeric time stamps) as an input feature can lead to a model that memorizes the actual timestamps instead of features that generalize to the future. This is disabled by default.

**Allow Date or Time Features to be Transformed Directly into a Numerical Representation**

Specify whether to allow Driverless AI to allow date or date-time features to be transformed by the DatesTransformer into a direct numeric value representing the floating point value of time. Note that this can lead to overfitting if used on IID problems. This is disabled by default.

**Consider Time Groups Columns as Standalone Features**

Specify whether to consider time groups columns as standalone features. This is disabled by default.

**Which TGC Feature Types to Consider as Standalone Features**

Specify whether to consider time groups columns (TGC) as standalone features. If “Consider time groups columns as standalone features” is enabled, then specify which TGC feature types to consider as standalone features. Available types are **numeric, categorical, ohe_categorical, datetime, date**, and **text**. All types are selected by default. 

Note that **“time_column”** is treated separately via the “Enable Feature Engineering from Time Column” option. Also note that if “Time Series Lag-Based Recipe” is disabled, then all time group columns are allowed features.

**Enable Time Unaware Transformers**

Specify whether various transformers (clustering, truncated SVD) are enabled, which otherwise would be disabled for time series experiments due to the potential to overfit by leaking across time within the fit of each fold. This is set to Auto by default.

**Always Group by All Time Groups Columns for Creating Lag Features**

Specify whether to group by all time groups columns for creating lag features. This is enabled by default.

**Generate Time-Series Holdout Predictions**

Specify whether to create holdout predictions on training data using moving windows. This can be useful for MLI, but it will slow down the experiment.

**Max Number of Splits Used for Creating Final Time-Series Model’s Holdout Predictions**

Specify the maximum number of splits used for creating the final time-series Model’s holdout predictions. This value defaults to 20.

**Dropout Mode for Lag Features**

Specify the dropout mode for lag features in order to achieve an equal n.a. ratio between train and validation/tests. Independent mode performs a simple feature-wise dropout. Dependent mode takes the lag-size dependencies per sample/row into account. Dependent is enabled by default.

**Probability to Create Non-Target Lag Features**

Lags can be created on any feature as well as on the target. Specify a probability value for creating non-target lag features. This value defaults to 0.1.

**Method to Create Rolling Test Set Predictions**

Specify the method used to create rolling test set predictions. Choose between test time augmentation (TTA) and a successive refitting of the final pipeline. TTA is enabled by default.

**Probability for New Time-Series Transformers to Use Default Lags**

Specify the probability for new lags or the EWMA gene to use default lags. This is determined independently of the data by frequency, gap, and horizon. This value defaults to 0.2.

**Probability of Exploring Interaction-Based Lag Transformers**

Specify the unnormalized probability of choosing other lag time-series transformers based on interactions. This value defaults to 0.2.

**Probability of Exploring Aggregation-Based Lag Transformers**

Specify the unnormalized probability of choosing other lag time-series transformers based on aggregations. This value defaults to 0.2.

**NLP Settings**

**Max TensorFlow Epochs for NLP**

When building TensorFlow NLP features (for text data), specify the maximum number of epochs to train feature engineering models with (it might stop earlier). The higher the number of epochs, the higher the run time. This value defaults to 2 and is ignored if TensorFlow models is disabled.

**Accuracy Above Enable TensorFlow NLP by Default for All Models**

Specify the accuracy setting. Values equal and above will add all enabled TensorFlow NLP models at the start of the experiment for text dominated problems. At lower accuracy, TensorFlow NLP transformations will only be created as a mutation. This value defaults to 5.

**Enable Word-Based CNN TensorFlow Models for NLP**

Specify whether to use Word-based CNN TensorFlow models for NLP. This option is ignored if TensorFlow is disabled. We recommend that you disable this option on systems that do not use GPUs.

**Enable Word-Based BiGRU TensorFlow Models for NLP**

Specify whether to use Word-based BiG-RU TensorFlow models for NLP. This option is ignored if TensorFlow is disabled. We recommend that you disable this option on systems that do not use GPUs.

**Enable Character-Based CNN TensorFlow Models for NLP**

Specify whether to use Character-level CNN TensorFlow models for NLP. This option is ignored if TensorFlow is disabled. We recommend that you disable this option on systems that do not use GPUs.

**Path to Pretrained Embeddings for TensorFlow NLP Models**

Specify a path to pretrained embeddings that will be used for the TensorFlow NLP models. For example, /path/on/server/to/file.txt

**Allow Training of Unfrozen Pretrained Embeddings**

Specify whether to allow training of all weights of the neural network graph, including the pretrained embedding layer weights. If this is disabled, the embedding layer will be frozen. All other weights, however, will still be fine-tuned. This is disabled by default.

**Whether Python/MOJO Scoring Runtime Will Have GPUs**

Specify whether the Python/MOJO scoring runtime will have GPUs (otherwise BiGRU will fail in production if this is enabled). Enabling this setting can speed up training for BiGRU, but doing so will require GPUs and CuDNN in production. This is disabled by default.

**Fraction of Text Columns Out of All Features to be Considered a Text-Dominated Problem**

Specify the fraction of text columns out of all features to be considered as a text-dominated problem. This value defaults to 0.3.

Specify when a string column will be treated as text (for an NLP problem) or just as a standard categorical variable. Higher values will favor string columns as categoricals, while lower values will favor string columns as text. This value defaults to 0.3.

**Fraction of Text per All Transformers to Trigger That Text Dominated**

Specify the fraction of text columns out of all features to be considered a text-dominated problem. This value defaults to 0.3.

**Threshold for String Columns to be Treated as Text**

Specify the threshold value (from 0 to 1) for string columns to be treated as text (0.0 - text; 1.0 - string). This value defaults to 0.3.

**Recipes Settings**

**Include Specific Transformers**

Select the transformer(s) that you want to use in the experiment.

**Include Specific Models**

Specify the type(s) of models that you want Driverless AI to build in the experiment.

**Include Specific Scorers**

Specify the scorer(s) that you want Driverless AI to include when running the experiment.

**Probability to Add Transformers**

Specify the unnormalized probability to add genes or instances of transformers with specific attributes. If no genes can be added, other mutations are attempted. This value defaults to 0.5.

**Probability to Add Best Shared Transformers**

Specify the unnormalized probability to add genes or instances of transformers with specific attributes that have shown to be beneficial to other individuals within the population. This value defaults to 0.5.

**Probability to Prune Transformers**

Specify the unnormalized probability to prune genes or instances of transformers with specific attributes. This value defaults to 0.5.

**Probability to Mutate Model Parameters**

Specify the unnormalized probability to change model hyper parameters. This value defaults to 0.25.

**Probability to Prune Weak Features**

Specify the unnormalized probability to prune features that have low variable importance instead of pruning entire instances of genes/transformers. This value defaults to 0.25.

**Timeout in Minutes for Testing Acceptance of Each Recipe**

Specify the number of minutes to wait until a recipe’s acceptance testing is aborted. A recipe is rejected if acceptance testing is enabled and it times out. This value defaults to 5.0.

**Whether to Skip Failures of Transformers**

Specify whether to avoid failed transformers. This is enabled by default.

**Whether to Skip Failures of Models**

Specify whether to avoid failed models. Failures are logged according to the specified level for logging skipped failures. This is enabled by default.

**Level to Log for Skipped Failures**

Specify one of the following levels for the verbosity of log failure messages for skipped transformers or models:

- 0 = Log simple message

- 1 = Log code line plus message (Default)

- 2 = Log detailed stack traces

**System Settings**

**Number of Cores to Use**

Specify the number of cores to use for the experiment. Note that if you specify 0, all available cores will be used. Lower values can reduce memory usage, but might slow down the experiment. This value defaults to 0.

**Maximum Number of Cores to Use for Model Fit**

Specify the maximum number of cores to use for a model’s fit call. Note that if you specify 0, all available cores will be used. This value defaults to 10.

**Maximum Number of Cores to Use for Model Predict**

Specify the maximum number of cores to use for a model’s predict call. Note that if you specify 0, all available cores will be used. This value defaults to 0.

**Maximum Number of Cores to Use for Model Transform and Predict When Doing MLI, Autoreport, Score on Another Dataset**

Specify the maximum number of cores to use for a model’s transform and predict call when doing operations in the Driverless AI MLI GUI. Note that if you specify 0, all available cores will be used. This value defaults to 2.

**Tuning Workers per Batch for CPU**

Specify the number of workers used in CPU mode for tuning. A value of 0 uses the socket count, while a value of -1 uses all physical cores greater than or equal to 1 that count. This value defaults to 0.

**Number of GPUs per Experiment**

Specify the number of GPUs to user per experiment. A value of -1 specifies to use all available GPUs. Must be at least as large as the number of GPUs to use per model (or -1).

**Number of GPUs per Model**

Specify the number of GPUs to user per model, with -1 meaning all GPUs per model. In all cases, XGBoost tree and linear models use the number of GPUs specified per model, while LightGBM and Tensorflow revert to using 1 GPU/model and run multiple models on multiple GPUs.

**Note**: FTRL does not use GPUs. Rulefit uses GPUs for parts involving obtaining the tree using LightGBM.

**Max Number of Threads to Use for datatable and OpenBLAS for Munging and Model Training**

Specify the maximum number of threads to use for datatable and OpenBLAS during data munging (applied on a per process basis). This value defaults to 4.

**GPU Starting ID**

Specify Which gpu_id to start with. If using CUDA\_VISIBLE\_DEVICES=… to control GPUs (preferred method), gpu_id=0 is the first in that restricted list of devices. For example, if CUDA\_VISIBLE\_DEVICES='4,5' then gpu_id_start=0 will refer to device #4.

From expert mode, to run 2 experiments, each on a distinct GPU out of 2 GPUs, then:

- Experiment#1: num\_gpus\_per\_model=1, num\_gpus\_per\_experiment=1, gpu\_id\_start=0

- Experiment#2: num\_gpus\_per\_model=1, num\_gpus\_per\_experiment=1, gpu\_id\_start=1

From expert mode, to run 2 experiments, each on a distinct GPU out of 8 GPUs, then:

- Experiment#1: num\_gpus\_per\_model=1, num\_gpus\_per\_experiment=4, gpu\_id\_start=0

- Experiment#2: num\_gpus\_per\_model=1, num\_gpus\_per\_experiment=4, gpu\_id\_start=4

To run on all 4 GPUs/model, then

- Experiment#1: num_gpus_per_model=4, num\_gpus\_per\_experiment=4, gpu\_id\_start=0

- Experiment#2: num\_gpus\_per\_model=4, num\_gpus\_per\_experiment=4, gpu\_id\_start=4

If num\_gpus\_per\_model!=1, global GPU locking is disabled. This is because the underlying algorithms do not support arbitrary gpu ids, only sequential ids, so be sure to set this value correctly to avoid overlap across all experiments by all users.

Note that gpu selection does not wrap, so gpu_id_start + num_gpus_per_model must be less than the number of visibile GPUs.

**Enable Detailed Traces**

Specify whether to enable detailed tracing in Driverless AI trace when running an experiment. This is disabled by default.

**Enable Debug Log Level**

If enabled, the log files will also include debug logs. This is disabled by default.

