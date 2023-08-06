Variable selection is inherently performed in Driverless AI because each model is trained on a subset of features.  During the Feature Evolution stage, Driverless AI uses a genetic algorithm to determine the best models.  In this experiment, there were {{experiment_overview._internal_args.num_individuals}} individuals that competed in feature evolution.
  
Each individual is made up of genes which decide the types of Feature Transformations that can be performed. The default list of genes is decided by Driverless AI’s expert data scientists.  During an iteration of the experiment, each individual creates a new model based on its genes.  These models are then evaluated by their {{ experiment.score_f_name }} on the validation data.   

In the genetic algorithm, the genes of the individual can change through mutation where genes can be added, pruned, or perturbed.  The strategy for adding genes is based on the importance of the original variables.  Genes will be added that explore additional transformations for original variables with high importance.  

The strategy for pruning genes is based on the Gain Based Variable Importance.  Variables are removed when Gain based variable importance is below a certain threshold.  In this experiment, the Gain based variable importance threshold is {{ feature_evolution.get_autodoc_varimp_threshold()}}.

Note: some genes may be added or pruned based on some random element, not the strategies described.

{% if config.fs_interpretability_switch <= params._params.interpretability %}

For this experiment, Driverless AI performed Feature Selection (FS) strategy due to the high interpretability setting.

The Feature Selection strategy occurs before the Feature Evolution stage.  Special individuals are created with carefully selected genes.  The genes are carefully selected using two possible methods: gene selection or variable selection.
 
Gene selection will remove a gene completely.  For example, if Truncated SVD is performed on [*ColumnA, ColumnB*] all columns from the Truncated SVD result would be dropped. Variable selection, on the other hand, will remove a specific variable such as *TruncSVD:ColumnA:ColumnB.0* (the first component of the Truncated SVD on *ColumnA* and *ColumnB*). Gene selection is more likely to cause underfitting, while variable selection is more likely to cause overfitting.

{% if fs_prune_by_genes %}

For this experiment, gene selection was performed.  During gene selection, the Permutation Based Variable Importance is calculated for all features created from a specific gene.  If these features are deemed low-importance (their permutation importance is less than a certain threshold), then the gene is completely removed from that individual and no features can be created from that gene.

{% else %}

For this experiment, variable selection was performed.  During variable selection, the Permutation Based Variable Importance is calculated for all features.  If any features are deemed low-importance (their permutation importance is less than a certain threshold), then the feature is removed.  

{% endif %}

{% endif %}

