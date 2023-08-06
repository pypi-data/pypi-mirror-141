**Deep Learning Models**

The following algorithm description comes directly from the \"Deep
Learning Overview\" section in H2O.ai\'s Deep Learning with H2O Booklet
(Candel et al. 9-10):

*Unlike the neural networks of the past, modern Deep Learning provides
training stability, generalization, and scalability with big data. Since
it performs quite well in several diverse problems, Deep Learning is
quickly becoming the algorithm of choice for the highest predictive
accuracy. *

*The first section is a brief overview of deep neural networks for
supervised learning tasks. There are several theoretical frameworks for
Deep Learning, but this document focuses primarily on the feedforward
architecture used by H2O.*

*The basic unit in the model is the neuron, a biologically inspired
model of the human neuron. In humans, the varying strengths of the
neurons\' output signals travel along the synaptic junctions and are
then aggregated as input for a connected neuron\'s activation.*

*In the model, the weighted combination*
$\alpha = \sum_{i = 1}^{n}{w_{i}x_{i}} + b$ *of input signals is
aggregated, and then an output signal* $f\left( \alpha \right)$
*transmitted by the connected neuron. The function* $f$ *represents the
nonlinear activation function used throughout the network and the bias,*
$b$*, represents the neuron\'s activation threshold.*

*Multi-layer, feedforward neural networks consist of many layers of
interconnected neuron units, starting with an input layer to match the
feature space, followed by multiple layers of nonlinearity, and ending
with a linear regression or classification layer to match the output
space. The inputs and outputs of the model\'s units follow the basic
logic of the single neuron described above.*

*Bias units are included in each non-output layer of the network. The
weights linking neurons and biases with other neurons fully determine
the output of the entire network. Learning occurs when these weights are
adapted to minimize the error on the labeled training data. More
specifically, for each training example* $j$*, the objective is to
minimize a loss function,*

$$L(W,B\ |\ j).$$

*Here,* $W$ *is the collection* $\left\{ W_{i} \right\}_{1:N - 1}$*,
where* $W_{i}$ *denotes the weight matrix connecting layers* $i$ *and*
$i + 1$ *for a network of* $N$ *layers. Similarly,* $B$ *is the
collection of* $\left\{ b_{i} \right\}_{1:N - 1}$*, where* $b_{i}$
*denotes the column vector of biases for layer* $i + 1$*.*

*This basic framework of multi-layer neural networks can be used to
accomplish Deep Learning tasks. Deep Learning architectures are models
of hierarchical feature extraction, typically involving multiple levels
of nonlinearity. Deep Learning models can learn useful representations
of raw data and have exhibited high performance on complex data such as
images, speech, and text (Bengio, 2009).*
