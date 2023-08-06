**Component Based Variable Importance** –The variable importance shown for the final model includes variables automatically created by Driverless AI.  To provide insight into the variable importance of the original variables, the variable importance is aggregated for all transformed variables derived from the selected variable in the final model.  Below is an example:

{{section.table(
    columns=['Variable', 'Variable Importance'],
    data=[
        ['NumToCatWoE:PAY_AMT2', '1'],
        ['PAY_3', '0.92'],
        ['ClusterDist9:BILL_AMT1:LIMIT_BAL:PAY_3', '0.90']
    ]
)}}

To calculate the variable importance of PAY\_3, we can aggregate the feature importance for all variables that used PAY\_3:

- **NumToCatWoE:PAY\_AMT2**: 1 * 0 (PAY\_3 not used)

- **PAY\_3**: 0.92 * 1 (PAY\_3 is the only variable used)

- **ClusterDist9:BILL\_AMT1:LIMIT\_BAL:PAY_3**: 0.90 * 1/3 (PAY\_3 is one of three variables used)

**Component Based Variable Importance** = (1 * 0) + (0.92 * 1) + (0.9 * (1/3)) = 1.22

**Note**: The variable importance is converted to relative variable importance.  (The variable with the highest estimated variable importance will have a relative variable importance of 1).

**Gain Based Variable Importance** – Gain based importance is calculated from the gains a specific variable brings to the model.  In the case of a decision tree, the Gain based importance will sum up the gains that occurred whenever the data was split by the given variable.  The Gain based importance is normalized between 0 and 1.  If a variable is never used in the model, the Gain based importance will be 0.

**Permutation Based Variable Importance** – Permutation based importance calculates variable importance based on how much worse the {{ experiment.score_f_name }} of the model would be if the selected variable was shuffled.  The {{ experiment.score_f_name }} of the model is recalculated with the shuffled variable and the difference in performance is used as a proxy for variable importance.  Variables that have a large impact on performance after shuffling are given higher performance.  The Permutation based importance is normalized between 0 and 1.

