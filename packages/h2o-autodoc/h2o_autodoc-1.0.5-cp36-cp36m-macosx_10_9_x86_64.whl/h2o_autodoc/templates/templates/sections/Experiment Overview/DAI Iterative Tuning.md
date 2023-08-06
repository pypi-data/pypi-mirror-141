#### Iterative Tuning
After the validation splits have been created, Driverless AI begins the iterative process of tuning models and transforming features to identify the parameters and features for the best model.

The next few sections sequentially discuss this iterative process.

**Target Tuning**

{{ section.render('Data Overview.DAI Target Transformation Description') }}

**Model and Feature Tuning**

During this stage, Driverless AI trains models with different parameters and different sets of selected features.

The goal from this step is to:

- Determine the best model and corresponding hyperparameters – the winning model and corresponding hyperparameters are then used in the Feature Evolution stage. If different types of models (XGBoost, GLM, etc.) are evaluated, the model with the best performance and training time is used during the Feature Evolution stage.

- Provide feature engineering information to the Feature Evolution stage. 

**Feature Evolution**

During this stage, Driverless AI uses a genetic algorithm to find the best set of features for the final model. These genetic algorithms not only decide which feature transformations, from the entire transformation space to apply, but also which transformations to keep, and whether to apply additional transformations to an already transformed feature.


**Transformations**

The genetic algorithm applies different types of transformations, depending on the problem type. For example, a times-series problem will have a different transformation search space than an NLP or independent-and-identically-distributed problem.

**Feature Tuning vs Feature Evolution**

This step may seem somewhat similar to the Feature Evolution stage since both stages are training models with different sets of features. The main difference between the Feature Tuning and Feature Evolution stages is how they decide which features to create: Feature Tuning uses variable importance in the previous iteration as a probabilistic prior to decide what new features to create, while the Feature Evolution stage uses a genetic algorithm.

**Stopping Criteria**

The Feature Evolution stage ends after a certain number of iterations, limited by the Time setting, or *Early Stopping* setting. Early stopping is triggered if the best set of features does not change for a certain number of iterations 

(Note: a model developer can control this iteration number or leave the default Driverless AI value).

