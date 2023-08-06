{% if scorers %}

**Additional Prediction Scores**

{{scorers.get_table()}}

{% endif %}

{% if gini_plot %} 

**Gini Plot**

The Gini Plot shows the equality line and the ROC curve for each dataset. The Gini metric for each dataset is provided in the legend.

{{gini_plot.plot()}}

{% endif %}

