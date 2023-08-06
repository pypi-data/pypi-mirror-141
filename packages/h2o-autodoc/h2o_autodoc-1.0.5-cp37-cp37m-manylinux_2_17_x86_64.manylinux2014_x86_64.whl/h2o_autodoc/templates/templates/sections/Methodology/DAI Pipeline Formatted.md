**Experiment Pipeline**

For this experiment, Driverless AI performed the following steps to find the optimal final model: 

{{images.dai_pipeline}} 

The steps in this pipeline are described in more detail below:

- **Ingest Data** {% if data_info._sampling_desc.downsampled %}
    - data filtered from {{"{:,}".format(train_data.row_count)}} to {{"{:,}".format(data_info._sampling_desc.sampled_size)}} rows using {{data_info._sampling_desc.sampling_type}} {% endif %}
    - detected column types 

-  **Feature Preprocessing**
    - turned raw features into numeric

- **Model and Feature Tuning**
    - This stage combines random hyperparameter tuning with feature selection and generation. Features in each iteration are updated using variable importance from the previous iteration as a probabilistic prior to decide what new features to create. The best performing model and features are then passed to the feature evolution stage.{% if experiment_overview._stage_info.get("Model and feature tuning").models != "None" %}
        - found the optimal parameters for {{model_tuning._tuning_algos|e}} by training models with different parameters
        - the best parameters are those that generate the {{scorer_direction}} {{experiment.score_f_name|e}} on the internal validation data {% else %}
        - performed no model tuning due to the Accuracy setting (consider increasing Accuracy setting) {% endif %} {% if experiment_overview._stage_info.get("Model and feature tuning").models != "None" %}
        - {{experiment_overview._stage_info.get("Model and feature tuning").models}}  model{% if experiment_overview._stage_info.get("Model and feature tuning").models > 1 %}s{%  endif %} trained and scored to evaluate features and model parameters {% endif %}


- **Feature Evolution**
    - This stage uses a genetic algorithm to find the best set of model parameters and feature transformations to be used in the final model.{% if experiment_overview._stage_info.get("Feature evolution").models == "None" %} 
    - trained no models during feature evolution because the user finished the experiment early {% else %}
    - found the best representation of the data for the final model training by creating and evaluating {{"{:,}".format(final_features.get_num_transformed_features_survived())}} features over {{experiment_overview._iteration_info.actual_num_iterations}} iteration{% if experiment_overview._iteration_info.actual_num_iterations > 1 %}s {% endif %}
    - trained and scored {{experiment_overview._stage_info.get("Feature evolution").models}} model{%  if experiment_overview._stage_info.get("Feature evolution").models > 1%}s{%  endif %} to further evaluate engineered features {% endif %}


- **Final Model** {% if final_model._final_model_type == "single model" %}
    - created the best model from the feature engineering iterations 
        - no stacked ensemble is done{% if experiment.valid_predictions_path == '' and (params._params.time_col == '[OFF]') %} due to accuracy or ensemble level settings (consider increasing accuracy or the ensemble_level) {% elif  params._params.time_col != '[OFF]' %} because a time column was provided {% elif experiment_overview._valid_data %} because a validation dataset was provided by the user{% else %} because the ensemble level was set to 0 {% endif %} {% elif final_model._final_model_type == "pasting ensemble" %}
        - the final model is a bagged ensemble (pasting) of {{final_model._final_model_string}} across {{final_model._num_folds}} folds.{% else %}
        - the final model is a stacked ensemble of {{final_model._final_model_string|e}}
        - the features of {% if final_model._num_ensemble_models > 1 %} these models {% else %} this model {% endif %} are the best features found during the feature engineering iterations {% endif %}

- **Create Scoring Pipeline** {% if experiment.mojo_pipeline_path != None %}
    - created and exported the MOJO and Python scoring pipeline
        - MOJO Scoring Pipeline: {{experiment.mojo_pipeline_path|e}}
        - Python Scoring Pipeline: {{experiment.scoring_pipeline_path|e}} {% else %}
        - created and exported the Python scoring pipeline (no MOJO Scoring Pipeline automatically created)
        - Python Scoring Pipeline: {{experiment.scoring_pipeline_path|e}} {% endif %}

**Models for Optimization**

Driverless AI trained models throughout the experiment to determine the best parameters, model dataset, and optimal final model. The stages are described below:

{{section.table(
    columns=['Driverless AI Stage', 'Timing (seconds)', 'Number of Models'],
    data=[
        ['Data Preparation', experiment_overview._stage_info.get("Data preparation").time, experiment_overview._stage_info.get("Data preparation").models],
        ['Model and Feature Tuning', experiment_overview._stage_info.get("Model and feature tuning").time, experiment_overview._stage_info.get("Model and feature tuning").models],
        ['Feature Evolution', experiment_overview._stage_info.get("Feature evolution").time, experiment_overview._stage_info.get("Feature evolution").models],
        ['Final Pipeline Training', experiment_overview._stage_info.get("Final pipeline training").time, experiment_overview._stage_info.get("Final pipeline training").models]
    ]
)}}
