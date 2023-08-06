This appendix is adapted from the Machine Learning Interpretability with H2O Driverless AI booklet; it provides explanations for each technique referenced in the Driverless AI Automatic Report. 

Driverless AI incorporates a number of contemporary approaches to increase the transparency and accountability of complex models and to enable users to debug models for accuracy and fairness including:
 
1. Decision tree surrogate models 

2. Individual conditional expectation (ICE) plots 

3. K local interpretable model-agnostic explanations (K-LIME)

4. Leave-one-covariate-out (LOCO) local feature importance 

5. Partial dependence plots 

6. Random forest feature importance 
This appendix covers the details of the interpretability techniques 1 – 5.

**Notation for Interpretability Techniques**

**Spaces**. Input features come from a $P$-dimensional input space $X$ (i.e. $X∈ℝ^P$). Output responses are in a $C$-dimensional output space $Y$ (i.e. $Y∈ℝ^C$).

**Dataset**. A dataset $D$ consists of $N$ tuples of observations:

$$[(\boldsymbol{x}^{(0)},\boldsymbol{y}^{(0)}),(\boldsymbol{x}^{(1)},\boldsymbol{y}^{(1)}),…,(\boldsymbol{x}^{(N-1)},\boldsymbol{y}^{(N-1)})], \boldsymbol{x}^{(i)}∈X,\boldsymbol{y}^{(i)}∈Y.$$

The input data can be represented as $X=[\boldsymbol{x}^{(0)},\boldsymbol{x}^{(1)},…,\boldsymbol{x}^{(N-1)}]$. With each $i$-th observation denoted as an instance $\boldsymbol{x}^{(i)}=[x_0^{(i)},x_1^{(i)},…,x_{P-1}^{(i)} ]$ of a feature set $P=\{X_0,X_1,…,X_{P-1}\}.$

**Decision Tree Surrogate Model**

A surrogate model is a data mining and engineering technique in which a generally simpler model is used to explain another usually more complex model or phenomenon. Given our learned function g and set of predictions, $g(X)=\widehat{Y}$, we can train a surrogate model $h: X,\widehat{Y}$, such that $h(X)≈g(X)$ . To preserve interpretability, the hypothesis set for h is often restricted to linear models or decision trees.

For the purposes of interpretation in Driverless AI, $g$ is considered to represent the entire pipeline, including both the feature transformations and model, and the surrogate model is a decision tree $(h_{tree})$. Model developers must also note that there exist few guarantees that $h_{tree}$ accurately represents $g$. The RMSE for $h_{tree}$ is displayed for assessing the fit between $h_{tree}$ and $g$.

$h_{tree}$ is used to increase the transparency of $g$ by displaying an approximate flow chart of the decision making process of $g$. The h_tree also shows the likely important features and the most important interactions in $g$. 

$h_{tree}$ can be used for visualizing, validating, and debugging $g$ by comparing the displayed decision-process, important features, and important interactions to known standards, domain knowledge, and reasonable expectations.

**Individual Conditional Expectation**

Individual conditional expectation (ICE) plots, a newer and less well-known adaptation of partial dependence plots, can be used to create more localized explanations for a single observation of data using the same basic ideas as partial dependence plots. ICE is also a type of nonlinear sensitivity analysis in which the model predictions for a single observation are measured while a feature of interest is varied over its domain.

Technically, ICE is a disaggregated partial dependence of the $N$ responses $g(X_j,\boldsymbol{x}_{(-j)}^{(i)}),i∈{1,…,N}$ (for a single feature $X_j$), instead of averaging the response across all observations of the training set . An ICE plot for a single observation $\boldsymbol{x}^{(i)}$ is created by plotting $g(X_j=x_{j,q},\boldsymbol{x}_{(-j)}^{(i)})$ versus $X_j=x_{j,q}, (q∈\{1,2,…\})$ while fixing $\boldsymbol{x}_{(-j)}^{(i)}$.

ICE plots enable a user to assess the Driverless AI model’s prediction for an individual observation of data, $g(\boldsymbol{x}^{(i)})$:

1. Is it outside one standard deviation from the average model behavior represented by partial dependence?

2. Is the treatment of a specific observation valid in comparison to average model behavior, known standards, domain knowledge, and reasonable expectations?
3. How will the observation behave in hypothetical situations where one feature, $X_j$, in a selected observation is varied across its domain?

**K local interpretable model-agnostic explanations**
K-LIME is a variant of the LIME technique proposed by Ribeiro et al . With K-LIME, local generalized linear model (GLM) surrogates are used to explain the predictions of complex response functions, and local regions are defined by K clusters or user-defined segments instead of simulated, perturbed observation samples. Currently in Driverless AI, local regions are segmented with K-means clustering, separating the input training data into K disjoint sets: $\{\boldsymbol{X}_0∪\boldsymbol{X}_1∪…\boldsymbol{X}_{K-1}\}=\boldsymbol{X}.$

For each cluster, a local GLM model $h_{GLM,k}$ is trained. $K$ is chosen such that predictions from all the local GLM models would maximize $R^2$.
 
K-LIME also trains one global surrogate GLM $h_{global}$ on the entire input training dataset and global model predictions $g(X)$. If a given $k$-th cluster has less than 20 members, then $h_{global}$ is used as a linear surrogate instead of $h_{GLM,k}$. Intercepts, coefficients, $R^2$ values, accuracy, and predictions from all the surrogate K-LIME models (including the global surrogate) can be used to debug and increase transparency in $g$.

In Driverless AI, global K-LIME information is available in the global ranked predictions plot and the global section of the explanations dialog. The parameters of $h_{global}$ give an indication of overall linear feature importance and the overall average direction in which an input feature influences $g$.

**KLIME Reason Codes**
For $h_{GLM,k}$ and observation $\boldsymbol{x}^{(i)}$: 

$$g(\boldsymbol{x}^{(i)})≈h_{GLM,k}({\boldsymbol{x}^{(i)}})=\beta_0^{[k]}+\sum_{p=1}^{P}{β_p^{[k]}}  x_p^{(i)}$$

By disaggregating the K-LIME predictions into individual coefficient-feature products, $\beta_p^{[k]}x_p^{(i)}$, the local, linear contribution of the feature can be determined. This coefficient-feature product is referred to as a reason code value and is used to create reason codes for each $g(\boldsymbol{x}^{(i)})$

**LOCO Feature Importance**

Leave-one-covariate-out (LOCO) provides a mechanism for calculating feature importance values for any model $g$ on a per-observation basis $\boldsymbol{x}^{(i)}$ by subtracting the model’s prediction for an observation of data, $g(\boldsymbol{x}^{(i)})$, from the model’s prediction for that observation of data without an input feature $X_j$ of interest, $g(\boldsymbol{x}^{(i)}_{(-j)}) - g(\boldsymbol{x}^{(i)})$. LOCO is a model-agnostic idea, and $g(\boldsymbol{x}^{(i)}_{(-j)})$ can be calculated in various ways. However, in Driverless AI, $g(\boldsymbol{x}^{(i)}_{(-j)})$ is currently calculated using a model-specific technique in which the contribution $X_j$ to $g(\boldsymbol{x}^{(i)})$ is approximated by using random forest surrogate model $h_{RF}$. Specifically, the prediction contribution of any rule $θ_r^{[b]}∈Θ_b$ containing ${X_j}$ for tree $h_{tree,b}$ is subtracted from the original prediction $h_{tree,b} (\boldsymbol{x}^{(i)};Θ_b)$. For the random forest:
$$g(\boldsymbol{x}^{(i)}_{(-j)})=h_{RF}(\boldsymbol{x}^{(i)}_{(-j)}) =\dfrac{1}{B} \sum_{b=1}^{B}{h_{tree,b}} (\boldsymbol{x}^{(i)};Θ_{b,(-j)} ),$$

where $Θ_{b,(-j)}$ is the set of splitting rules for each tree $h_{tree,b}$ with the contributions of all rules involving feature $X_j$ removed. Although LOCO feature importance values can be signed quantities, they are scaled between 0 and 1 such that the most important feature for an observation of data, $\boldsymbol{x}^{(i)}$, has an importance value of 1 for direct global versus local comparison to random forest feature importance in Driverless AI.

**Partial Dependence Plots**

For a $P$-dimensional feature space, we can consider a single feature $X_j∈P$ and its complement set $X_{(-j)}$ (i.e $X_j∪X_{(-j)}=P$). The one-dimensional partial dependence of a function $g$ on $X_j$ is the marginal expectation:
$$PD(X_j,g)=\mathbb{E}_{X_{(-j)}} [g(X_j,X_{(-j)})]$$

Recall that the marginal expectation over $X_{(-j)}$ sums over the values of $X_{(-j)}$. Now we can explicitly write one-dimensional partial dependence as:

$$PD(X_j,g)=\mathbb{E}_{X_{(-j)}} [g(X_j,X_{(-j)})]=\dfrac{1}{N} \sum_{i=1}^N{g(X_j,\boldsymbol{x}^{(i)}_{(-j)})}
$$

This equation essentially states that the partial dependence of a given feature $X_j$ is the average of the response function g, setting the given feature $X_j=x_j$ and using all other existing feature vectors of the complement set $\boldsymbol{x}^{(i)}_{(-j)}$ as they exist in the dataset.

Partial dependence plots show the partial dependence as a function of specific values of our feature subset $X_j$. The plots show how machine-learned response functions change based on the values of an input feature of interest, while taking nonlinearity into consideration and averaging out the effects of all other input features. Partial dependence plots enable increased transparency in $g$ and enable the ability to validate and debug $g$ by comparing a feature’s average predictions across its domain to known standards and reasonable expectations.

