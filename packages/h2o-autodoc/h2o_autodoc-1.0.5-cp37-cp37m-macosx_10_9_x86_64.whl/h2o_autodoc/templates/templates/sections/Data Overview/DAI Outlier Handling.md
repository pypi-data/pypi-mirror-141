**Outlier Handling**

Driverless AI does not remove outliers from the input data. Instead, Driverless AI finds the best way to represent data with outliers. For example, Driverless AI may find that binning a variable with outliers improves performance. For target columns, Driverless AI first determines the best representation of the column. It may find that for a target column with outliers, it is best to predict the log of the column.

{% if final_features.get_transformation_category('Numeric to Categorical Target Encoding|Numeric to Categorical Weight of Evidence') != None %}

For the *{{experiment.description}}* experiment, Driverless AI applied the following numeric transformations which involve binning. 

{{final_features.get_transformation_category('Numeric to Categorical Target Encoding|Numeric to Categorical Weight of Evidence')}}

{% else %} 

For the *{{experiment.description}}* experiment, Driverless AI did not apply any transformations to features of numeric type.

{% endif %}