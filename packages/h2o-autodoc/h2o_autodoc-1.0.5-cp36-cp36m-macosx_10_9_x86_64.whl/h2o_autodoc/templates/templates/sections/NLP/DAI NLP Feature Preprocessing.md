{% if nlp.get_descriptions() %}

**NLP Transformations**

Driverless AI applied NLP-model-based transformations to text features in the dataset. The description of the transformations and corresponding model architecture are detailed below:

{% for description in nlp.get_descriptions() %}

#### {{ description.name }}

{{ description.description}}

**Architecture**

`{{description.architecture}}`

{% if 'embedding' in description.keys()%}

{{ description.embedding}}

{% endif %}

{% endfor%}

{% endif %}

