**eXtreme Gradient Boosting: XGBoost**

The following algorithm description is taken directly from the H2O.ai
H2O-3 User Guide
(https://docs.h2o.ai/h2o/latest-stable/h2o-docs/index.html):

*XGBoost (Chen and Guestrin 2016) is a supervised learning algorithm
that implements a process called boosting to yield accurate models.
Boosting refers to the ensemble learning technique of building many
models sequentially, with each new model attempting to correct for the
deficiencies in the previous model. In tree boosting, each new model
that is added to the ensemble is a decision tree. To enhance machine
learning speed and performance, the XGBoost package implements novel
techniques for boosting trees in parallel.*

*The H2O XGBoost implementation is based on two separated modules (Note:
there are no algorithmic differences between H2O XGBoost and native
XGBoost; H2O calls the regular XGBoost backend. The first module,
h2o-genmodel-ext-xgboost, extends module h2o-genmodel and registers an
XGBoost-specific MOJO. The module also contains all necessary XGBoost
binary libraries. The module can contain multiple libraries for each
platform to support different configurations (e.g., with/without
GPU/OMP). H2O always tries to load the most powerful one (currently a
library with GPU and OMP support). If it fails, then the loader tries
the next one in a loader chain. For each platform, H2O provide an
XGBoost library with minimal configuration (supports only single CPU)
that serves as fallback in case all other libraries could not be
loaded.*

*The second module, h2o-ext-xgboost, contains the actual XGBoost model
and model builder code, which communicates with native XGBoost libraries
via the JNI API. The module also provides all necessary REST API
definitions to expose the XGBoost model builder to clients.*

*XGBoost in H2O supports multicore, thanks to OpenMP. The multicore
implementation will only be available if the system itself supports it.
(It has the right version of libraries.) If the requirements are not
satisfied, XGBoost will use a fallback that is single core only.*

***{% if final_model._is_dart_booster%}XGBoost with Dart Booster***

*XGBoost DART was introduced to prevent XGBoost GBM's
"over-specialization," where newly added trees only focus on correcting
a few observations that may not improve the overall ensemble's
performance. Instead of fitting a new tree with respect to all previous
trees, DART selects one with respect to a random subset of the previous
trees. A scaling factor is then applied to the new tree, to account for
the dropped trees. To enhance machine learning speed and performance,
the XGBoost package implements novel techniques for boosting trees in
parallel. The step to randomly select a subset of trees, however, can
cause XGBoost DART to be slower than XGBoost GBM, because it requires
the gradients and residuals to be recalculated.{% endif %}*
