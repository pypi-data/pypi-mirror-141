{% if experiment.scoring_pipeline_path != None and experiment.mojo_pipeline_path != None %}

For this experiment, both Python and MOJO Scoring Pipelines are available for productionizing the final model pipeline for a given row of data or table of data. 

{% elif experiment.scoring_pipeline_path != None %}

For this experiment, the Python Scoring Pipeline is available for productionizing the final model pipeline for a given row of data or table of data. The MOJO Scoring Pipeline can be built by clicking the **BUILD MOJO SCORING PIPELINE** button if available. 

{% else %}

For this experiment, the MOJO Scoring Pipeline is available for productionizing the final model pipeline for a given row of data or table of data. The Python Scoring Pipeline is not available.

{% endif %} 

{% if experiment.scoring_pipeline_path != None %}

### Python Scoring Pipeline

This package contains an exported model and Python 3.6 source code examples for productionizing models built using H2O Driverless AI. The Python Scoring Pipeline is located here:

- **{{experiment.scoring_pipeline_path|e}}**

The files in this package allow you to transform and score on new data in a couple of different ways:

- From Python 3.6, you can import a scoring module, then use the module to transform and score on new data.

- From other languages and platforms, you can use the TCP/HTTP scoring service bundled with this package to call into the scoring pipeline module through remote procedure calls (RPC). 

{% endif %}

{% if experiment.mojo_pipeline_path != None %}


### MOJO Scoring Pipeline

Note: The MOJO Scoring Pipeline is currently in a beta state. Updates and improvements will continue to be made in subsequent Driverless AI releases. The MOJO Scoring Pipeline is located here: 

- **{{experiment.mojo_pipeline_path|e}}**

For completed experiments, Driverless AI converts models to MOJOs (Model Objects, Optimized). A MOJO is a scoring engine that can be deployed in any Java environment for scoring in real time.

{% endif %}

