**Generalized Linear Models**

The following algorithm description comes directly from the
\"Generalized Linear Models\" section in H2O.ai\'s Generalized Linear
Modeling with H2O Booklet (Nykodym et al. 9-10):

*Generalized linear models (GLMs) are an extension of traditional linear
models. They have gained popularity in statistical data analysis due to
the flexibility of the model structure unifying the typical regression
methods (such as linear regression and logistic regression for binary
classification), the recent availability of model-fitting software, and
the ability to scale well with large datasets.*

***Model Components***

*The estimation of the model is obtained by maximizing the
log-likelihood over the parameter vector* $\beta$ *for the observed
data:*

$$\operatorname{}\mathrm{\ (\ GLM\ Log - likelihood)}$$

*In the familiar linear regression setup, the independent observations
vector* $y$ *is assumed to be related to its corresponding predictor
vector* $x$ *by* $y = x^{\top}\beta + \beta_{0} + \ \epsilon$*, where*
$\beta$ *is the parameter vector,* $\beta_{0}$ *represents the intercept
term and* $\epsilon \sim \mathcal{N}\left( 0,\sigma^{2} \right)$ *is a
gaussian random variable which is the noise in the model.*

*The response* $y$ *is normally distributed*
$y \sim \mathcal{N}\left( x^{\top}\beta + \beta_{0},\sigma^{2} \right)$
*as well. Since it assumes additivity of the covariates, normality of
the error term as well as constancy of the variance, this model is
restrictive. Because these assumptions are not applicable to many
problems and datasets, a more flexible model is beneficial.*

*GLMs relax the above assumptions by allowing the variance to vary as a
function of the mean, non-normal errors and a non-linear relation
between the response and covariates. More specifically, the response
distribution is assumed to belong to the exponential family, which
includes the Gaussian, Poisson, binomial, multinomial and gamma
distributions as special cases. *

*The components of a GLM are:*

-   *The random component* $f$ *for the dependent variable* $y$*: the
    density function* $f(y;\theta,\phi)$ *has a probability distribution
    from the exponential family parametrized by* $\theta$ *and* $\phi$*.
    This removes the restriction on the distribution of the error and
    allows for non-homogeneity of the variance with respect to the mean
    vector.*

-   *The systematic component (linear model)* $\eta$*:*
    $\eta = X\beta$*, where* $X$ *is the matrix of all observation
    vectors* $x_{i}$*.*

-   *The link function* $g$*:* $E(y) = \mu = g^{-}1(\eta)$ *which
    relates the expected value of the response* $\mu$ *to the linear
    component* $\eta$*. The link function can be any monotonic
    differentiable function. This relaxes the constraints on the
    additivity of the covariates, and it allows the response to belong
    to a restricted range of values depending on the chosen
    transformation* $g$*.*

*This generalization makes GLM suitable for a wider range of problems.
An example of a case of the GLM representation is the familiar logistic
regression model commonly used for binary classification in medical
applications.*
