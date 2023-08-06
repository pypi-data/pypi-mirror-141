{% if not final_model._h2o%}

**Pipeline**

{{final_model._ensemble_json.get("ensemble.txt")|e}}{% if "pipeline" in images.keys()%}

{{images.pipeline}}

{% endif %}{% if "experiment_lineage" in images.keys()%}

**Model Lineage**

The following plot shows the experiment lineage for the current experiment {{experiment.description|e}}.

{{images.experiment_lineage}}

{% endif %}

**Details**

- The fitted features of the final model are the best features found during the feature engineering iterations. 

- The target transformer indicates the type of transformation applied to the target column. 

{% else %}

{% endif %}

{{section.render('Final Model.Pipeline Overview')}}

For a complete list of the parameters of the final model, see the Appendix.