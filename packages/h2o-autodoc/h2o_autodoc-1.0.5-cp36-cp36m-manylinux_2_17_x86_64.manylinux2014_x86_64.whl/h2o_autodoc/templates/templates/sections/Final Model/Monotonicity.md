{% if final_model.monotonicity_constraints | length > 0 %}**Monotonicity Constraints**

Monotonicity constraints enforce a monotonic relationship between a specified feature and target prediction. A +1 value enforces an increasing monotonic relationship and a -1 value enforces a decreasing monotonic relationship. Note that constraints can only be defined for numeric columns.

**Note:** In GBM and XGBoost, this option can only be used when the distribution is either *'gaussian'* or *'bernoulli'*.

These are the constraints defined by the model:

{{final_model.monotonicity_constraints}}
{% endif %}
