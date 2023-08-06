{% if mli.has_dt() %}The decision tree surrogate model is used to increase the transparency of the Driverless AI model by displaying an approximate flow-chart of the complex Driverless AI model’s decision-making process.  The surrogate Decision Tree is a decision tree whose predictors are the original variables in the data.  The goal of the decision tree is to predict the final Driverless AI model’s prediction.

The thickness of the splits in the graph indicate how many records follow that path.

{{mli.get_decision_tree_plot ()}}{% endif %}
