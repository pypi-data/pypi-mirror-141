The Driverless AI experiment automatically created {{final_features.get_num_transformed_features_survived()}} new features and selected {{final_features.get_num_transformed_features_used()}} of them to be used in the final model. The table below shows a portion of the variables considered over the {{experiment_overview._iteration_info.actual_num_iterations}} iterations.  

The table below shows the transformed features created by Driverless AI for the best model in each iteration.  The table is limited to the transformed features that were found to be significant to the model (within the top 15 features).

{{feature_evolution.get_top_features_iterations(10)}}