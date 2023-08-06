{% if nlp.get_descriptions() %}

**NLP-Model-Based Feature Transformations**

{{images.nlp_pipeline}} 

Driverless AI applies a multi-stage approach to processing text data and engineering new text-based features. The flow chart above depicts a two-stage process. The first step shows techniques to transform text features into numeric features. These include term frequency-inverse document frequency (TF-IDF), n-gram frequency, and word embeddings. The second step either applies a dimensionality reduction technique or builds a cross-validated model with the numeric features as input and the experiment's target as output. The final column shows the naming convention for these NLP-based features.

**Stage Summaries**:

- **TF-IDF of n-grams**: Term frequency–inverse document frequency (TF-IDF) vectors for n-grams, where n-grams can be single or multiple pairs or consecutive words. 

- **Frequency of n-grams**: Term frequency vectors for n-grams, where n-grams can be a single word or multiple consecutive words.

- **Word embeddings**: a learned representation of words, in which words from the vocabulary are mapped to vectors of real numbers. Representations are made so that words with similar meanings are placed close to or equidistant from one another. For example, the word “king” is closely associated with the word “queen” in this kind of vector representation.

- **Linear Model with TF-IDF features**: a new feature set is generated from the cross-validated predictions of a linear model  that takes  TF-IDF features as input and tries to predict the experiment's original target.  These new features can help capture linear dependencies between the original text features and the target.  

- **Word-based Convolutional Neural Networks (CNN)**: Cross-validated predictions of a CNN model using word embeddings are used to generate new text-based features. CNNs for text-based machine learning tasks have proven to be efficient and fast when compared to RNN models.

- **Word-based  Bidirectional GRU**: A bidirectional GRU model combines two independent RNN models into a single model. A GRU architecture provides high speeds and accuracy rates similar to a LSTM architecture. As with CNN models, this model takes word embeddings as input and returns cross-validated predictions that can be used as a new set of features. 

- **Character-level Convolutional Neural Networks (CNN)**: Character-level CNNs can be helpful when the input text data contains character-based languages like Japanese or Chinese. Cross-validated predictions of a CNN model using character embeddings are used to generate new text-based features.

{% endif %}

