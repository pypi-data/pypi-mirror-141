The model's performance is evaluated using {% if valid_strat.method ==
'not_n_folds' %}{{valid_strat.frame}} with shape {{
valid_strat.shape}}{% else %}{{valid_strat.nfolds}}-fold cross
validation, where the fold assignment is based on
{{valid_strat.fold_assignment}}. Cross validation creates K + 1 models
(i.e., {{valid_strat.nfolds + 1}} in this case): K cross-validated
models, and 1 final model built on the entire dataset{% endif %}.

{% if final_model._glm_in_final %}The following table shows the parameters which control early stopping in a GLM:

{{ final_model._glm_early_stop_tbl }}

- When **early\_stopping** is enabled, GLM will automatically stop building a model when there is no more relative improvement on the training or validation (if provided) set. This option prevents expensive model building with many predictors when no more improvements are occurring.


- The **max\_active\_predictors** option limits the number of active predictors. (Note that the actual number of non-zero predictors in the model is going to be slightly lower). This is useful when obtaining a sparse solution to avoid costly computation of models with too many predictors.

{% else %} Early stopping ends model training when the selected
"stopping metric" does not improve for a specified number of training
rounds, based on a simple moving average. {% if
valid_strat.early_stopping %} For example, this model has the
following early stopping configurations:

-   stopping\_rounds: **{{valid_strat.stopping_rounds}}**

-   stopping\_metric: **{{valid_strat.stopping_metric}}**

-   stopping\_tolerance: **{{valid_strat.stopping_tolerance}}**

This means the moving average for the last
***{{valid_strat.stopping_rounds + 1}}*** stopping rounds is
calculated (the first moving average is a reference value to which the
other ***{{valid_strat.stopping_rounds}}*** moving averages are
compared).

The model is set to stop building if the
***{{valid_strat.stopping_metric}}*** doesn't improve by ***{{
valid_strat.stopping_tolerance }}*** after
***{{valid_strat.stopping_rounds}}*** stopping rounds. Specifically,
this model stops building, if the ratio between the best moving average
and the reference moving average {{ valid_strat.ineq_str}} ***1 {{
valid_strat.ineq_sign}} {{valid_strat.stopping_tolerance}}***. These
stopping configurations restrict the number of model iterations in order
to increase the model's performance.{% else %} For this model, early
stopping is disabled during training.{% endif %}{% endif %}
