During the experiment, Driverless AI trained {{"{:,}".format(alternative_models._num_alternative_models | int)}} alternative models. The following algorithms were evaluated during the Driverless AI experiment:

{{alternative_models._algo_details.package_details}}

Driverless AI can evaluate an array of algorithms, including but not limited to XGBoost GBM, XGBoost Dart, XGBoost GLM, LightGBM, RuleFit, Tensorflow, and FTRL models. The table below explains why certain algorithms were not selected for the final model, if any.

{{alternative_models._algo_selection}}

