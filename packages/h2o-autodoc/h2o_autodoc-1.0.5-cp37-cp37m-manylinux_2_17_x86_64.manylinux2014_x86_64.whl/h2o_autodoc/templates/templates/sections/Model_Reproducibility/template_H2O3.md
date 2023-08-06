{% if model_reproducibility.reproducible%}To reproduce this
{{final_model. _final_model_string}} on a {{
model_reproducibility.cluster_type}} cluster, train a model using the
same: datasets, model parameters, and cluster configuration.

**Datasets**

Make sure the model is trained on the same datasets. The datasets are the same if it they have the same hash{% set hash_dict = model_reproducibility.hash %}{% if not hash_dict %}.{% else %}: {% for key in hash_dict %}

-	{{key}}: {{hash_dict.get(key)}} {% endfor %}{% endif %}


The *h2o.frame()* function, which retrieves metadata for an H2OFrame's
id, can be used to verify a dataset's hash:

*{{model_reproducibility.code_example() }}*

**Note:** Reproducibility is only guaranteed for single-file imports.
H2O-3 may shuffle the data during a multi-file directory import, and
therefore reproducibility cannot be guaranteed.

**Model Parameters**

The same model parameters and H2O-3 version must be used to reproduce
this model. Parameters set to 'AUTO' use the version's default values
and should not be set by the user.

{{version_info}}

{{model_reproducibility.model_params}}                                                                           

{% if model_reproducibility.sampling_enabled%}

**Sampling Parameters**

The same seed and sampling parameters are required, as sampling is
enabled for this model.

{{model_reproducibility.model_sampling_params}}                                                                                    

{% endif %}

**Cluster Configuration**

The same cluster configuration is required.

{{model_reproducibility.cluster_configuration}}                                                                                    

**Node Order**

The cluster's leader node must trigger the model training.

{{model_reproducibility.node_order}}                                                                         

**Note:** When H2O-3 is running on Hadoop, the h2odriver automatically
returns the leader node to which the user should connect. In multi-node
deployments of Standalone H2O-3, the user must identify the leader node.
Flow users can easily check whether they are connected to the leader
node by opening Cluster Status (from the Admin menu) and checking that
the first node has the same IP address as they see in their browser's
address bar.

{% else %}This model is not reproducible, because early stopping was
enabled without setting the **score\_tree\_interval** parameter.

**Early Stopping Parameters**

{{model_reproducibility.early_stopping_params}}                                                                                    

**Single-Node Cluster Reproducibility Requirements**

The following criteria must be met to guarantee reproducibility in a
single node cluster:

-   Same training data. **Note**: If you have H2O-3 import a whole
    directory with multiple files instead of a single file, H2O-3 does
    not guarantee reproducibility because the data may be shuffled
    during import.

-   Same parameters are used to train the model.

-   Same seed is used if sampling is done. The following parameters
    perform sampling:

	-   sample\_rate
	
	-   sample\_rate\_per\_class
	
	-   col\_sample\_rate
	
	-   col\_sample\_rate\_change\_per\_level
	
	-   col\_sample\_rate\_per\_tree


-   No early stopping performed or early stopping
    with score\_tree\_interval is explicitly specified and the same
    validation data.

**Multi-Node Cluster Reproducibility Requirements**

The following criteria must be met to guarantee reproducibility in a
multi-node cluster:

-   Reproducible requirements for single node cluster are met. (See
    above.)

-   The cluster configuration is the same:
	
	-   Clusters must have the same number of nodes.
	
	-   Nodes must have the same number of CPU cores available (or same
	    restriction on number of threads).

If you do not have a machine with the same number of CPU cores, see the
question "How can I reproduce a model if machines have a different
number of CPU cores?" below.

-   The model training is triggered from the leader node of the cluster.
    (See note below.)

**Note**: When H2O is running on Hadoop, the leader node is
automatically returned by the h2odriver as the node that the user should
connect to. In multi-node deployments of Standalone H2O, the leader node
must be manually identified by the user. Flow users can easily check
whether they are connected to the leader node by opening Cluster Status
(from the Admin menu) and checking that the first node has the same IP
address as they see in their browser's address bar. {% endif %}
