{% if params._params.time_col != '[OFF]' %}

Time series was enabled for this experiment using the following settings:

{{section.table(
    columns=['Setting', 'Value'],
    data=[
        ['Time Column',  params._params.time_col ],
        ['Time Group Column',  params._params.time_groups_columns ],
        ['Time Period',  params._params.time_unit],
        ['Number of Prediction Periods',  params._params.num_prediction_periods],
        ['Number of Gap Periods',  params._params.num_gap_periods]
    ]
)}}

#### Time Series Table Definitions

**Time Column**: this option allows a model developer to specify a time-based column in their dataset.  When a time column is selected, Driverless AI feature engineering and model validation respects the causality of time. If the Time Column is set to OFF, no time order is used for modeling and data may be shuffled randomly (any potential temporal causality will be ignored).

**Time Group Columns**: this option is used to specify which columns make up the time series groups. 

**Time Period**: this option specifies the periodicity found in the dataset.

**Number of Prediction Periods**: this option specifies the number of periods a model developer wants to predict in advance.

**Number of Gap Periods**: this option specifies the gap between the data available and the forecast period desired.

{% endif %}

